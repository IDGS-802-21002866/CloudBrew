from werkzeug.security import generate_password_hash

from app import db
from app.modules.clientes.model import Cliente
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
    id_venta, id_producto_venta, cantidad, precio_unitario, subtotal
):
    detalle = DetalleVenta(
        id_venta=id_venta,
        id_producto_venta=id_producto_venta,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=subtotal,
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


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()
