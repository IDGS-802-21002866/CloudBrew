import random
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from flask import current_app, render_template, session, url_for
from flask_login import login_user, logout_user
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash

from app import mail
from app.modules.producto_venta.model import ProductoVenta
from app.modules.inventario_producto_terminado.service import (
    InventarioProductoTerminadoService,
)
from app.modules.tienda import repository
from app.modules.usuarios.repository import (
    actualizar_password,
    get_usuario_by_email,
    get_usuario_by_reset_token,
    guardar_token_recuperacion,
    limpiar_token_recuperacion,
)


inventario_service = InventarioProductoTerminadoService()

# Tiempo que dura una reserva de stock desde que se agrega al carrito
RESERVA_TTL_MINUTOS = 30


def _get_session_id():
    """Devuelve (y crea si no existe) el identificador único de la sesión del carrito."""
    if "tienda_session_id" not in session:
        session["tienda_session_id"] = str(uuid.uuid4())
        session.modified = True
    return session["tienda_session_id"]


class TiendaAuthService:
    def registrar_cliente(self, data):
        try:
            usuario = repository.create_usuario_cliente(data)
            repository.create_cliente_web(data)
            repository.commit()
            return usuario
        except ValueError:
            repository.rollback()
            raise
        except Exception:
            repository.rollback()
            raise ValueError("Error inesperado al registrar el cliente.")

    def iniciar_sesion(self, correo, contrasenia):
        usuario = repository.get_usuario_cliente_by_email(correo)

        if not usuario:
            raise ValueError("Credenciales incorrectas.")

        if not usuario.activo:
            raise ValueError("Tu cuenta está deshabilitada.")

        if not check_password_hash(usuario.password, contrasenia):
            raise ValueError("Credenciales incorrectas.")

        # Validar que el usuario SÍ sea cliente
        if usuario.rol.name != "cliente":
            raise ValueError(
                "Esta cuenta no tiene acceso al portal de tienda. Por favor, usa el sistema administrativo."
            )

        codigo = f"{random.randint(0, 999999):06d}"
        session["codigo_2fa"] = codigo
        session["codigo_2fa_expiry"] = (
            datetime.now(timezone.utc) + timedelta(minutes=5)
        ).isoformat()
        session["usuario_2fa_id"] = usuario.id

        msg = Message(
            subject="Código de verificación - CloudBrew",
            recipients=[usuario.email],
            html=render_template(
                "tienda/correo_2fa.html",
                nombre=usuario.nombre,
                codigo=codigo,
            ),
        )
        mail.send(msg)

        return True

    def verificar_codigo_2fa(self, codigo):
        codigo_guardado = session.get("codigo_2fa")
        expiry_str = session.get("codigo_2fa_expiry")
        usuario_id = session.get("usuario_2fa_id")

        if not codigo_guardado or not expiry_str or not usuario_id:
            raise ValueError("No hay un código de verificación pendiente.")

        expiry = datetime.fromisoformat(expiry_str)
        if datetime.now(timezone.utc) > expiry:
            self._limpiar_session_2fa()
            raise ValueError("El código ha expirado. Inicia sesión nuevamente.")

        if codigo != codigo_guardado:
            raise ValueError("El código es incorrecto.")

        from app.modules.usuarios.repository import get_usuario_by_id

        usuario = get_usuario_by_id(usuario_id)
        if not usuario or not usuario.activo:
            self._limpiar_session_2fa()
            raise ValueError("Usuario no válido.")

        login_user(usuario)
        self._limpiar_session_2fa()
        return usuario

    def cerrar_sesion(self):
        logout_user()

    def solicitar_recuperacion(self, correo):
        usuario = repository.get_usuario_cliente_by_email(correo)
        if not usuario or not usuario.activo:
            raise ValueError("Correo inválido.")

        token = secrets.token_urlsafe(32)
        expiry = datetime.now(timezone.utc) + timedelta(hours=1)
        guardar_token_recuperacion(usuario, token, expiry)

        enlace = url_for("tienda.restablecer_contrasena", token=token, _external=True)
        msg = Message(
            subject="Recuperar contraseña - CloudBrew",
            recipients=[usuario.email],
            html=render_template(
                "auth/correo_recuperacion.html",
                enlace=enlace,
                nombre=usuario.nombre,
            ),
        )
        mail.send(msg)

    def restablecer_contrasena(self, token, nueva_contrasenia):
        usuario = get_usuario_by_reset_token(token)
        if not usuario:
            raise ValueError("El enlace de recuperación no es válido.")

        expiry = usuario.reset_token_expiry
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expiry:
            raise ValueError("El enlace de recuperación ha expirado.")

        actualizar_password(usuario, generate_password_hash(nueva_contrasenia))
        limpiar_token_recuperacion(usuario)

    def _limpiar_session_2fa(self):
        session.pop("codigo_2fa", None)
        session.pop("codigo_2fa_expiry", None)
        session.pop("usuario_2fa_id", None)


class TiendaProductoService:
    def _stock_disponible_packs(self, producto, session_id=None):
        """Packs que otras sesiones NO han reservado.
        Se usa como base para validar cuánto puede reservar esta sesión en total."""
        repository.limpiar_reservas_expiradas()
        stock_receta = float(
            inventario_service.obtener_stock_actual_receta(producto.receta_id) or 0
        )
        reservado = repository.get_unidades_reservadas_por_receta(
            producto.receta_id, excluir_session_id=session_id
        )
        stock_neto = max(stock_receta - reservado, 0)
        return (
            int(stock_neto // producto.cantidad_unidades)
            if producto.cantidad_unidades > 0
            else 0
        )

    def _stock_agregable_packs(self, producto, session_id):
        """Packs que el usuario AÚN puede agregar al carrito.
        = máximo reservable para esta sesión - lo que ya tiene reservado."""
        stock_libre_para_sesion = self._stock_disponible_packs(producto, session_id)
        reserva_propia = repository.get_reserva_by_session_producto(
            session_id, producto.id
        )
        stock_max_para_sesion = stock_libre_para_sesion + (
            reserva_propia.cantidad_packs if reserva_propia else 0
        )
        ya_en_carrito = reserva_propia.cantidad_packs if reserva_propia else 0
        return max(stock_max_para_sesion - ya_en_carrito, 0)

    def listar_productos_disponibles(self):
        session_id = _get_session_id()
        repository.limpiar_reservas_expiradas()
        productos = []
        for producto in ProductoVenta.query.filter_by(tipo="web", activo=True).all():
            # Packs que puede agregar AÚN (descontando su propio carrito)
            stock_agregable = self._stock_agregable_packs(producto, session_id)
            # Para mostrar en la lista también incluimos lo que ya tiene en carrito
            reserva_propia = repository.get_reserva_by_session_producto(
                session_id, producto.id
            )
            stock_total_para_usuario = stock_agregable + (
                reserva_propia.cantidad_packs if reserva_propia else 0
            )
            if stock_total_para_usuario > 0:
                productos.append(
                    {
                        "id": producto.id,
                        "receta_id": producto.receta_id,
                        "receta_nombre": producto.receta.nombre,
                        "nombre": producto.nombre,
                        "descripcion": producto.descripcion,
                        "precio_venta": float(producto.precio_venta),
                        "stock_actual": stock_total_para_usuario,
                        "stock_agregable": stock_agregable,
                        "tiene_imagen": producto.receta.imagen is not None,
                    }
                )
        return productos

    def obtener_producto(self, producto_venta_id):
        producto = ProductoVenta.query.get(producto_venta_id)
        if not producto or not producto.activo or producto.tipo != "web":
            raise ValueError("Producto no encontrado.")

        session_id = _get_session_id()
        stock_agregable = self._stock_agregable_packs(producto, session_id)
        reserva_propia = repository.get_reserva_by_session_producto(
            session_id, producto.id
        )
        stock_total_para_usuario = stock_agregable + (
            reserva_propia.cantidad_packs if reserva_propia else 0
        )

        return {
            "id": producto.id,
            "receta_id": producto.receta_id,
            "receta_nombre": producto.receta.nombre,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio_venta": producto.precio_venta,
            "stock_actual": stock_total_para_usuario,
            "stock_agregable": stock_agregable,
            "tiene_imagen": producto.receta.imagen is not None,
        }

    def obtener_receta_con_presentaciones(self, receta_id):
        """Obtiene una receta con todas sus presentaciones disponibles (para el detalle)."""
        session_id = _get_session_id()
        repository.limpiar_reservas_expiradas()
        productos_web = ProductoVenta.query.filter_by(
            receta_id=receta_id, tipo="web", activo=True
        ).all()

        if not productos_web:
            raise ValueError("Producto no encontrado.")

        presentaciones = []
        for producto in productos_web:
            stock_agregable = self._stock_agregable_packs(producto, session_id)
            reserva_propia = repository.get_reserva_by_session_producto(
                session_id, producto.id
            )
            stock_total = stock_agregable + (
                reserva_propia.cantidad_packs if reserva_propia else 0
            )
            presentaciones.append(
                {
                    "id": producto.id,
                    "nombre": producto.nombre,
                    "precio_venta": float(producto.precio_venta),
                    "cantidad_unidades": producto.cantidad_unidades,
                    "stock_agregable": stock_agregable,
                    "stock_total": stock_total,
                    "presentacion_nombre": (
                        producto.presentacion.nombre
                        if producto.presentacion
                        else producto.nombre
                    ),
                }
            )

        presentaciones_disponibles = [p for p in presentaciones if p["stock_total"] > 0]
        if not presentaciones_disponibles:
            raise ValueError("Producto no encontrado.")

        receta = productos_web[0].receta
        return {
            "receta_id": receta_id,
            "receta_nombre": receta.nombre,
            "descripcion": productos_web[0].descripcion,
            "tiene_imagen": receta.imagen is not None,
            "presentaciones": presentaciones_disponibles,
        }


class TiendaCarritoService:
    CARRITO_KEY = "tienda_carrito"
    _producto_service = None

    @property
    def _svc(self):
        if self._producto_service is None:
            self._producto_service = TiendaProductoService()
        return self._producto_service

    def obtener_carrito(self):
        return session.get(self.CARRITO_KEY, [])

    def agregar_producto(self, producto_venta_id, cantidad):
        session_id = _get_session_id()
        carrito = self.obtener_carrito()

        producto = ProductoVenta.query.get(producto_venta_id)
        if not producto or not producto.activo or producto.tipo != "web":
            raise ValueError("Producto no disponible.")

        # Calcular la nueva cantidad total que el usuario quiere tener en el carrito
        cantidad_actual_en_carrito = next(
            (
                i["cantidad"]
                for i in carrito
                if i["producto_venta_id"] == producto_venta_id
            ),
            0,
        )
        cantidad_total_este_producto = cantidad_actual_en_carrito + cantidad

        # VALIDACIÓN ROBUSTA: Considerar todas las reservas de esta sesión para esta receta
        # Calcular unidades totales ya reservadas para otros productos de la misma receta
        repository.limpiar_reservas_expiradas()
        unidades_reservadas_otros_productos = 0.0

        otros_productos_receta = ProductoVenta.query.filter_by(
            receta_id=producto.receta_id, tipo="web", activo=True
        ).all()

        for otro_prod in otros_productos_receta:
            if otro_prod.id != producto.id:  # No incluir este producto
                reserva = repository.get_reserva_by_session_producto(
                    session_id, otro_prod.id
                )
                if reserva:
                    unidades_reservadas_otros_productos += reserva.cantidad_unidades

        # Unidades que este producto intenta reservar
        unidades_este_producto = (
            cantidad_total_este_producto * producto.cantidad_unidades
        )

        # Unidades ya reservadas para ESTE producto (a reemplazar)
        reserva_actual_este = repository.get_reserva_by_session_producto(
            session_id, producto.id
        )
        unidades_reservadas_este_actual = (
            reserva_actual_este.cantidad_unidades if reserva_actual_este else 0
        )

        # Stock total disponible de la receta
        stock_receta = float(
            inventario_service.obtener_stock_actual_receta(producto.receta_id) or 0
        )

        # Calcular el nuevo total si se agrega este producto
        unidades_totales_con_este_producto = (
            unidades_reservadas_otros_productos + unidades_este_producto
        )

        if unidades_totales_con_este_producto > stock_receta:
            disponible_para_este = max(
                stock_receta - unidades_reservadas_otros_productos, 0
            )
            disponible_packs = int(disponible_para_este // producto.cantidad_unidades)
            raise ValueError(
                f"Stock insuficiente para '{producto.nombre}'. "
                f"Disponible: {disponible_packs} packs ({disponible_para_este:.0f} unidades), "
                f"Solicitado: {cantidad_total_este_producto} packs ({unidades_este_producto:.0f} unidades)."
            )

        # Crear o actualizar la reserva en BD
        expiry = datetime.utcnow() + timedelta(minutes=RESERVA_TTL_MINUTOS)
        repository.crear_o_actualizar_reserva(
            session_id=session_id,
            producto_venta_id=producto.id,
            receta_id=producto.receta_id,
            cantidad_packs=cantidad_total_este_producto,
            cantidad_unidades=unidades_este_producto,
            expiry=expiry,
        )
        repository.commit()

        # Actualizar carrito en sesión
        for item in carrito:
            if item["producto_venta_id"] == producto_venta_id:
                item["cantidad"] = cantidad_total_este_producto
                session[self.CARRITO_KEY] = carrito
                session.modified = True
                return carrito

        carrito.append(
            {
                "producto_venta_id": producto.id,
                "receta_id": producto.receta_id,
                "nombre": producto.nombre,
                "precio_unitario": float(producto.precio_venta),
                "cantidad": cantidad_total_este_producto,
                "tiene_imagen": producto.receta.imagen is not None,
            }
        )
        session[self.CARRITO_KEY] = carrito
        session.modified = True
        return carrito

    def actualizar_cantidad(self, producto_venta_id, cantidad):
        session_id = _get_session_id()
        carrito = self.obtener_carrito()

        for item in carrito:
            if item["producto_venta_id"] == producto_venta_id:
                if cantidad <= 0:
                    carrito.remove(item)
                    repository.eliminar_reserva(session_id, producto_venta_id)
                    repository.commit()
                else:
                    producto = ProductoVenta.query.get(producto_venta_id)
                    if not producto:
                        break

                    # VALIDACIÓN ROBUSTA: Considerar todas las reservas de esta sesión para esta receta
                    repository.limpiar_reservas_expiradas()
                    unidades_reservadas_otros_productos = 0.0

                    otros_productos_receta = ProductoVenta.query.filter_by(
                        receta_id=producto.receta_id, tipo="web", activo=True
                    ).all()

                    for otro_prod in otros_productos_receta:
                        if otro_prod.id != producto.id:
                            reserva = repository.get_reserva_by_session_producto(
                                session_id, otro_prod.id
                            )
                            if reserva:
                                unidades_reservadas_otros_productos += (
                                    reserva.cantidad_unidades
                                )

                    unidades_esta_linea = cantidad * producto.cantidad_unidades
                    stock_receta = float(
                        inventario_service.obtener_stock_actual_receta(
                            producto.receta_id
                        )
                        or 0
                    )

                    unidades_totales = (
                        unidades_reservadas_otros_productos + unidades_esta_linea
                    )

                    if unidades_totales > stock_receta:
                        disponible_para_este = max(
                            stock_receta - unidades_reservadas_otros_productos, 0
                        )
                        disponible_packs = int(
                            disponible_para_este // producto.cantidad_unidades
                        )
                        raise ValueError(
                            f"Stock insuficiente para '{item['nombre']}'. "
                            f"Disponible: {disponible_packs} packs ({disponible_para_este:.0f} unidades), "
                            f"Solicitado: {cantidad} packs ({unidades_esta_linea:.0f} unidades)."
                        )

                    expiry = datetime.utcnow() + timedelta(minutes=RESERVA_TTL_MINUTOS)
                    repository.crear_o_actualizar_reserva(
                        session_id=session_id,
                        producto_venta_id=producto.id,
                        receta_id=producto.receta_id,
                        cantidad_packs=cantidad,
                        cantidad_unidades=unidades_esta_linea,
                        expiry=expiry,
                    )
                    repository.commit()
                    item["cantidad"] = cantidad
                break

        session[self.CARRITO_KEY] = carrito
        session.modified = True
        return carrito

    def eliminar_producto(self, producto_venta_id):
        session_id = _get_session_id()
        carrito = self.obtener_carrito()
        carrito = [i for i in carrito if i["producto_venta_id"] != producto_venta_id]
        repository.eliminar_reserva(session_id, producto_venta_id)
        repository.commit()
        session[self.CARRITO_KEY] = carrito
        session.modified = True
        return carrito

    def obtener_total(self):
        carrito = self.obtener_carrito()
        return sum(i["precio_unitario"] * i["cantidad"] for i in carrito)

    def obtener_cantidad_items(self):
        carrito = self.obtener_carrito()
        return sum(i["cantidad"] for i in carrito)

    def limpiar_carrito(self):
        session_id = session.get("tienda_session_id")
        if session_id:
            repository.eliminar_reservas_de_sesion(session_id)
            repository.commit()
        session.pop(self.CARRITO_KEY, None)
        session.pop("tienda_session_id", None)
        session.modified = True


class TiendaCheckoutService:
    def confirmar_compra(self, usuario):
        carrito_service = TiendaCarritoService()
        carrito = carrito_service.obtener_carrito()

        if not carrito:
            raise ValueError("El carrito está vacío.")

        cliente = repository.get_cliente_by_email(usuario.email)
        if not cliente:
            raise ValueError("No se encontró el perfil de cliente.")

        total = 0.0
        detalles_validados = []
        producto_service = TiendaProductoService()

        # Validar stock TOTAL por receta (no por producto individual)
        # Agrupar por receta_id para validar el total de unidades
        recetas_totales = {}  # {receta_id: total_unidades}

        for item in carrito:
            producto = ProductoVenta.query.get(item["producto_venta_id"])
            if not producto:
                raise ValueError(f"Producto '{item['nombre']}' ya no está disponible.")

            # Calcular unidades totales para esta línea del carrito
            unidades_esta_linea = item["cantidad"] * producto.cantidad_unidades

            # Sumar al total de la receta
            if producto.receta_id not in recetas_totales:
                recetas_totales[producto.receta_id] = 0.0
            recetas_totales[producto.receta_id] += unidades_esta_linea

        # Ahora validar que cada receta tiene suficiente stock
        for receta_id, unidades_totales in recetas_totales.items():
            stock_actual = float(
                inventario_service.obtener_stock_actual_receta(receta_id) or 0
            )
            if stock_actual < unidades_totales:
                # Obtener nombre de la receta para el mensaje
                from app.modules.recetas.model import Recetas

                receta = Recetas.query.get(receta_id)
                receta_nombre = receta.nombre if receta else "Producto"
                raise ValueError(
                    f"Stock insuficiente para '{receta_nombre}'. "
                    f"Disponible: {stock_actual:.2f} unidades, Solicitado: {unidades_totales:.2f} unidades."
                )

        # Stock validado, procesar cada línea del carrito
        for item in carrito:
            producto = ProductoVenta.query.get(item["producto_venta_id"])

            subtotal = item["precio_unitario"] * item["cantidad"]
            total += subtotal
            detalles_validados.append(
                {
                    "producto_venta_id": item["producto_venta_id"],
                    "cantidad": item["cantidad"],
                    "precio_unitario": item["precio_unitario"],
                    "subtotal": subtotal,
                }
            )

        try:
            venta = repository.create_venta_web(cliente.id, total)

            for detalle in detalles_validados:
                repository.create_detalle_venta(
                    id_venta=venta.id,
                    id_producto_venta=detalle["producto_venta_id"],
                    cantidad=detalle["cantidad"],
                    precio_unitario=detalle["precio_unitario"],
                    subtotal=detalle["subtotal"],
                )

                producto = ProductoVenta.query.get(detalle["producto_venta_id"])
                unidades_vendidas = detalle["cantidad"] * producto.cantidad_unidades
                repository.create_movimiento_receta(
                    receta_id=producto.receta_id,
                    tipo="salida",
                    cantidad=unidades_vendidas,
                    motivo=f"Venta web #{venta.id} - {producto.nombre}",
                    usuario_id=usuario.id,
                )

            repository.commit()
            carrito_service.limpiar_carrito()
            return venta
        except Exception as e:
            repository.rollback()
            raise ValueError(f"Error al procesar la compra: {str(e)}")
