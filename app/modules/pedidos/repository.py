from app import db
from sqlalchemy import or_
from app.modules.pedidos.model import Pedido, PedidoDetalle
from app.modules.clientes.model import Cliente


def get_all_pedidos():
    return Pedido.query.all()


def get_pedido_by_id(pedido_id):
    return Pedido.query.get(pedido_id)


def get_paginated_pedidos(page, per_page, search_term=None):
    query = Pedido.query.join(Cliente)

    if search_term:
        # Buscamos en las columnas reales: nombres O apellidos
        query = query.filter(
            or_(
                Cliente.nombres.ilike(f"%{search_term}%"),
                Cliente.apellidos.ilike(f"%{search_term}%")
            )
        )

    return query.order_by(Pedido.fecha_registro.desc()).paginate(page=page, per_page=per_page)


def save(pedido):
    db.session.add(pedido)
    db.session.commit()
    return pedido


def commit():
    db.session.commit()


def get_clientes_retail():
    from app.modules.clientes.model import Cliente
    return Cliente.query.filter(Cliente.tipo == 'retail', Cliente.activo == True).all()
