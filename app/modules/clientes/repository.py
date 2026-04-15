from app.modules.clientes.model import Cliente
from app import db


def create_cliente_desde_usuario(usuario):
    """Crea un registro mínimo de cliente a partir de un usuario con rol=cliente creado desde el ERP."""
    nombres = usuario.nombre.strip().split(" ", 1)
    nuevo_cliente = Cliente(
        nombres=nombres[0].title(),
        apellidos=nombres[1].title() if len(nombres) > 1 else "",
        email=usuario.email,
        calle_numero="Por definir",
        colonia="Por definir",
        ciudad="Por definir",
        estado="Por definir",
        codigo_postal="00000",
        tipo="erp",
        activo=True,
        usuario_id=usuario.id,
    )
    db.session.add(nuevo_cliente)
    db.session.commit()
    return nuevo_cliente


def get_all_clientes():
    return Cliente.query.all()


def get_cliente_by_id(id):
    return Cliente.query.get(id)


def get_cliente_by_email(email):
    return Cliente.query.filter(Cliente.email == email).first()


def create_cliente(cliente):
    db.session.add(cliente)
    db.session.commit()
    return cliente


def update_db():
    db.session.commit()


def update_cliente(cliente):
    db.session.commit()


def deactivate_cliente(cliente):
    cliente.activo = False
    db.session.commit()


def get_paginated_clientes(page, per_page, search_term=None):
    query = Cliente.query

    if search_term:
        query = query.filter(
            (Cliente.nombres.ilike(f"%{search_term}%"))
            | (Cliente.apellidos.ilike(f"%{search_term}%"))
        )

    return query.order_by(Cliente.fecha_registro.desc()).paginate(
        page=page, per_page=per_page
    )
