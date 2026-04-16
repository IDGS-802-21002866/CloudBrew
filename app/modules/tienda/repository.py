from datetime import datetime, timezone

from sqlalchemy import func
from werkzeug.security import generate_password_hash

from app import db
from app.modules.clientes.model import Cliente
from app.modules.inventario_producto_terminado.model import MovimientosReceta
from app.modules.tienda.model import ReservaStock
from app.modules.usuarios.model import Rol, Usuario
from app.modules.ventas.model import DetalleVenta, Venta


def get_rol_cliente():
    return Rol.query.filter_by(name="cliente").first()


def get_usuario_cliente_by_email(email):
    rol = get_rol_cliente()
    if not rol:
        return None
    return Usuario.query.filter_by(email=email, rol_id=rol.id).first()


def create_usuario_cliente(data):
    rol = get_rol_cliente()
    if not rol:
        raise ValueError("El rol 'cliente' no existe en el sistema.")

    existente = Usuario.query.filter_by(email=data["email"]).first()
    if existente:
        raise ValueError("Ya existe un usuario con ese email.")

    nuevo_usuario = Usuario(
        nombre=f"{data['nombres']} {data['apellidos']}",
        email=data["email"],
        password=generate_password_hash(data["contrasenia"]),
        rol_id=rol.id,
        activo=True,
    )
    db.session.add(nuevo_usuario)
    db.session.flush()
    return nuevo_usuario


def create_cliente_web(data):
    existente = Cliente.query.filter_by(email=data["email"]).first()
    if existente:
        raise ValueError("Ya existe un cliente con ese email.")

    nuevo_cliente = Cliente(
        nombres=data["nombres"].strip().title(),
        apellidos=data["apellidos"].strip().title(),
        email=data["email"].strip().lower(),
        telefono=data.get("telefono"),
        calle_numero=data["calle_numero"].strip(),
        colonia=data["colonia"].strip(),
        ciudad=data["ciudad"].strip(),
        estado=data["estado"].strip(),
        codigo_postal=data["codigo_postal"].strip(),
        tipo="web",
    )
    db.session.add(nuevo_cliente)
    db.session.flush()
    return nuevo_cliente


def get_cliente_by_email(email):
    return Cliente.query.filter_by(email=email).first()


def create_venta_web(id_cliente, total):
    venta = Venta(
        id_cliente=id_cliente,
        tipo="web",
        total=total,
    )
    db.session.add(venta)
    db.session.flush()
    return venta


def create_detalle_venta(
    id_venta, id_producto_venta, cantidad, precio_unitario
):
    detalle = DetalleVenta(
        id_venta=id_venta,
        id_producto_venta=id_producto_venta,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
    )
    db.session.add(detalle)
    return detalle


def get_ventas_by_cliente(id_cliente):
    return (
        Venta.query.filter_by(id_cliente=id_cliente, tipo="web")
        .order_by(Venta.fecha.desc())
        .all()
    )


def get_venta_by_id(id_venta):
    return Venta.query.get(id_venta)


def create_movimiento_receta(receta_id, tipo, cantidad, motivo, usuario_id):
    movimiento = MovimientosReceta(
        receta_id=receta_id,
        tipo=tipo,
        cantidad=cantidad,
        motivo=motivo,
        usuario_id=usuario_id,
    )
    db.session.add(movimiento)
    return movimiento


# ── Reservas de stock ────────────────────────────────────────────────────────


def limpiar_reservas_expiradas():
    """Elimina todas las reservas cuya vigencia ya venció."""
    ahora = datetime.utcnow()
    ReservaStock.query.filter(ReservaStock.expiry < ahora).delete()


def get_reserva_by_session_producto(session_id, producto_venta_id):
    return ReservaStock.query.filter_by(
        session_id=session_id,
        producto_venta_id=producto_venta_id,
    ).first()


def get_unidades_reservadas_por_receta(receta_id, excluir_session_id=None):
    """Suma las unidades reservadas vigentes para una receta, opcionalmente
    excluyendo la sesión indicada (la propia sesión del usuario)."""
    ahora = datetime.utcnow()
    query = ReservaStock.query.filter(
        ReservaStock.receta_id == receta_id,
        ReservaStock.expiry > ahora,
    )
    if excluir_session_id:
        query = query.filter(ReservaStock.session_id != excluir_session_id)
    resultado = query.with_entities(func.sum(ReservaStock.cantidad_unidades)).scalar()
    return float(resultado or 0)


def crear_o_actualizar_reserva(
    session_id, producto_venta_id, receta_id, cantidad_packs, cantidad_unidades, expiry
):
    reserva = get_reserva_by_session_producto(session_id, producto_venta_id)
    if reserva:
        reserva.cantidad_packs = cantidad_packs
        reserva.cantidad_unidades = cantidad_unidades
        reserva.expiry = expiry
    else:
        reserva = ReservaStock(
            session_id=session_id,
            producto_venta_id=producto_venta_id,
            receta_id=receta_id,
            cantidad_packs=cantidad_packs,
            cantidad_unidades=cantidad_unidades,
            expiry=expiry,
        )
        db.session.add(reserva)
    return reserva


def eliminar_reserva(session_id, producto_venta_id):
    ReservaStock.query.filter_by(
        session_id=session_id,
        producto_venta_id=producto_venta_id,
    ).delete()


def eliminar_reservas_de_sesion(session_id):
    ReservaStock.query.filter_by(session_id=session_id).delete()


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()
