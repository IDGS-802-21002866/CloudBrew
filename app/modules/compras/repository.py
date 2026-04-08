from app.modules.compras.model import Compra, DetalleCompra
from app import db


def get_all_compras():
    compras = Compra.query.all()
    return compras


def get_compra_by_id(id):
    compra = Compra.query.get(id)
    return compra


def create_compra(proveedor_id, usuario_id, detalles):
    """
    Crear una nueva compra con sus detalles.

    Args:
        proveedor_id: ID del proveedor
        usuario_id: ID del usuario
        detalles: lista de dicts con {materia_prima_id, presentacion_id, cantidad, precio_unitario}

    Returns:
        ID de la compra creada
    """
    # Crear la compra
    nueva_compra = Compra(proveedor_id=proveedor_id, usuario_id=usuario_id)

    db.session.add(nueva_compra)
    db.session.flush()  # Flush para obtener el ID sin hacer commit

    # Crear los detalles
    for detalle in detalles:
        nuevo_detalle = DetalleCompra(
            compra_id=nueva_compra.id,
            materia_prima_id=detalle.get("materia_prima_id"),
            presentacion_id=detalle.get("presentacion_id"),
            cantidad=detalle.get("cantidad"),
            precio_unitario=detalle.get("precio_unitario", 0),
        )
        db.session.add(nuevo_detalle)

    db.session.commit()
    return nueva_compra.id


def update_compra():
    db.session.commit()


def confirmar_compra(compra_id, detalle_precios, fecha_compra):
    """
    Actualiza precios de los detalles y la fecha de compra en una sola transacción.

    Args:
        compra_id: ID de la compra a confirmar
        detalle_precios: lista de tuplas (detalle_id, precio_unitario)
        fecha_compra: fecha de la compra (date)
    """
    compra = Compra.query.get(compra_id)
    if compra:
        compra.fecha_compra = fecha_compra

    for detalle_id, precio in detalle_precios:
        detalle = DetalleCompra.query.get(detalle_id)
        if detalle:
            detalle.precio_unitario = precio

    db.session.commit()


def cancelar_compra(compra_id):
    compra = Compra.query.get(compra_id)
    if compra:
        compra.cancelada = True
        db.session.commit()
