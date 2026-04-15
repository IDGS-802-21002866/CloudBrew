import random
import secrets
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
    def listar_productos_disponibles(self):
        inventario = inventario_service.listar_recetas_con_stock()
        stock_por_receta = {
            item["id"]: float(item["stock_actual"] or 0) for item in inventario
        }
        productos = []
        for producto in ProductoVenta.query.filter_by(tipo="web", activo=True).all():
            stock_receta = stock_por_receta.get(producto.receta_id, 0)
            stock_packs = (
                int(stock_receta // producto.cantidad_unidades)
                if producto.cantidad_unidades > 0
                else 0
            )
            if stock_packs > 0:
                productos.append(
                    {
                        "id": producto.id,
                        "receta_id": producto.receta_id,
                        "nombre": producto.nombre,
                        "descripcion": producto.descripcion,
                        "precio_venta": float(producto.precio_venta),
                        "stock_actual": stock_packs,
                        "tiene_imagen": producto.receta.imagen is not None,
                    }
                )
        return productos

    def obtener_producto(self, producto_venta_id):
        producto = ProductoVenta.query.get(producto_venta_id)
        if not producto or not producto.activo or producto.tipo != "web":
            raise ValueError("Producto no encontrado.")

        stock_receta = float(
            inventario_service.obtener_stock_actual_receta(producto.receta_id) or 0
        )
        stock_packs = (
            int(stock_receta // producto.cantidad_unidades)
            if producto.cantidad_unidades > 0
            else 0
        )

        return {
            "id": producto.id,
            "receta_id": producto.receta_id,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio_venta": producto.precio_venta,
            "stock_actual": stock_packs,
            "tiene_imagen": producto.receta.imagen is not None,
        }


class TiendaCarritoService:
    CARRITO_KEY = "tienda_carrito"

    def obtener_carrito(self):
        return session.get(self.CARRITO_KEY, [])

    def agregar_producto(self, producto_venta_id, cantidad):
        carrito = self.obtener_carrito()

        for item in carrito:
            if item["producto_venta_id"] == producto_venta_id:
                item["cantidad"] += cantidad
                session[self.CARRITO_KEY] = carrito
                session.modified = True
                return carrito

        producto = ProductoVenta.query.get(producto_venta_id)
        if not producto or not producto.activo or producto.tipo != "web":
            raise ValueError("Producto no disponible.")

        carrito.append(
            {
                "producto_venta_id": producto.id,
                "receta_id": producto.receta_id,
                "nombre": producto.nombre,
                "precio_unitario": producto.precio_venta,
                "cantidad": cantidad,
                "tiene_imagen": producto.receta.imagen is not None,
            }
        )
        session[self.CARRITO_KEY] = carrito
        session.modified = True
        return carrito

    def actualizar_cantidad(self, producto_venta_id, cantidad):
        carrito = self.obtener_carrito()
        for item in carrito:
            if item["producto_venta_id"] == producto_venta_id:
                if cantidad <= 0:
                    carrito.remove(item)
                else:
                    item["cantidad"] = cantidad
                break
        session[self.CARRITO_KEY] = carrito
        session.modified = True
        return carrito

    def eliminar_producto(self, producto_venta_id):
        carrito = self.obtener_carrito()
        carrito = [i for i in carrito if i["producto_venta_id"] != producto_venta_id]
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
        session.pop(self.CARRITO_KEY, None)
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

        for item in carrito:
            stock_receta = float(
                inventario_service.obtener_stock_actual_receta(item["receta_id"]) or 0
            )
            producto = ProductoVenta.query.get(item["producto_venta_id"])
            cantidad_unidades = producto.cantidad_unidades if producto else 1
            stock_packs = (
                int(stock_receta // cantidad_unidades) if cantidad_unidades > 0 else 0
            )

            if stock_packs < item["cantidad"]:
                raise ValueError(
                    f"Stock insuficiente para '{item['nombre']}'. "
                    f"Disponible: {stock_packs}, Solicitado: {item['cantidad']}."
                )

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

            repository.commit()
            carrito_service.limpiar_carrito()
            return venta
        except Exception:
            repository.rollback()
            raise ValueError("Error al procesar la compra.")
