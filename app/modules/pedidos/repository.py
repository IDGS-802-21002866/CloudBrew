from app import db
from sqlalchemy import or_
from app.modules.pedidos.model import Pedido, PedidoDetalle
from app.modules.clientes.model import Cliente
from app.modules.sol_prod.model import PedidoProduccion


def get_all_pedidos():
    return Pedido.query.all()


def get_pedido_by_id(pedido_id):
    return Pedido.query.get(pedido_id)


def get_paginated_pedidos(page, per_page, search_term=None):
    query = Pedido.query.join(Cliente)

    if search_term:
        query = query.filter(
            or_(
                Cliente.nombres.ilike(f"%{search_term}%"),
                Cliente.apellidos.ilike(f"%{search_term}%"),
            )
        )

    return query.order_by(Pedido.fecha_registro.desc()).paginate(
        page=page, per_page=per_page
    )


def create_pedido(cliente_id, detalles, total=None):
    """
    Crea un pedido con sus detalles. Solo flush, sin commit.

    Args:
        cliente_id: ID del cliente
        detalles: lista de dicts con {receta_id, cantidad_lotes, total_unidades, precio_unitario}
        total: monto total del pedido

    Returns:
        Pedido creado (sin commit)
    """
    nuevo_pedido = Pedido(cliente_id=cliente_id, total=total)
    db.session.add(nuevo_pedido)
    db.session.flush()

    for detalle in detalles:
        detalle_pedido = PedidoDetalle(
            pedido_id=nuevo_pedido.id,
            receta_id=detalle["receta_id"],
            cantidad_lotes=detalle["cantidad_lotes"],
            total_unidades=detalle["total_unidades"],
            precio_unitario=detalle.get("precio_unitario"),
        )
        db.session.add(detalle_pedido)

    return nuevo_pedido


def create_pedido_produccion(pedido_id, produccion_id):
    pedido_produccion = PedidoProduccion(
        id_pedido=pedido_id,
        id_produccion=produccion_id,
    )
    db.session.add(pedido_produccion)


def update_pedido_estado(pedido, estado):
    pedido.estado = estado
    db.session.commit()


def save(pedido):
    db.session.add(pedido)
    db.session.commit()
    return pedido


def commit():
    db.session.commit()


def get_clientes_retail():
    from app.modules.clientes.model import Cliente

    return Cliente.query.filter(Cliente.tipo == "retail", Cliente.activo == True).all()


def get_producciones_by_pedido(pedido_id):
    return PedidoProduccion.query.filter_by(id_pedido=pedido_id).all()
