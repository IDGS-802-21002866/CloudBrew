from app.modules.compras.model import Compra, DetalleCompra, SolicitudCompra
from app import db
from app.modules.proveedores.model import Proveedor


def get_all_compras():
    compras = Compra.query.all()
    return compras
from sqlalchemy import or_

def get_paginated_compras(page, per_page, search_term=None, terminadas=False):
    query = Compra.query.join(Proveedor)
    if search_term:
        query = query.filter(
            or_(
                Proveedor.nombre.ilike(f"%{search_term}%"),
            )
        )
    if terminadas:
        query = query.filter(Compra.fecha_compra.is_not(None))
    else:
        query = query.filter(Compra.fecha_compra.is_(None))

    return query.order_by(Compra.fecha_registro.desc()).paginate(
        page=page,
        per_page=per_page
    )

def get_pending_solicitudes():
    return SolicitudCompra.query.filter_by(estado="Pendiente").all()


def get_solicitudes_confirmadas_retail():
    return SolicitudCompra.query.filter(
        SolicitudCompra.origen == "retail",
        SolicitudCompra.estado == "Surtida",
    ).all()


def get_solicitudes_surtidas_retail():
    return SolicitudCompra.query.filter(
        SolicitudCompra.origen == "retail",
        SolicitudCompra.estado == "Surtida",
    ).all()


def get_confirmed_compras():
    return Compra.query.filter(Compra.fecha_compra.isnot(None), Compra.cancelada == False).all()


def get_solicitud_by_id(solicitud_id):
    return SolicitudCompra.query.get(solicitud_id)


def mark_solicitud_estado(solicitud_id, estado):
    solicitud = SolicitudCompra.query.get(solicitud_id)
    if solicitud:
        solicitud.estado = estado
        db.session.add(solicitud)
        db.session.commit()


def create_solicitud(materia_prima_id, cantidad, origen="retail", referencia_id=None):
    solicitud = SolicitudCompra(
        materia_prima_id=materia_prima_id,
        cantidad=cantidad,
        origen=origen,
        referencia_id=referencia_id,
        estado="Pendiente",
    )
    db.session.add(solicitud)
    db.session.flush()
    return solicitud


def get_compra_by_id(id):
    compra = Compra.query.get(id)
    return compra


def create_compra(proveedor_id, usuario_id, detalles, usuario_actual):
    """
    Crear una nueva compra con sus detalles.

    Args:
        proveedor_id: ID del proveedor
        usuario_id: ID del usuario
        detalles: lista de dicts con {materia_prima_id, presentacion_id, cantidad, precio_unitario}
        usuario_actual: nombre del usuario actual

    Returns:
        ID de la compra creada
    """
    # Crear la compra
    nueva_compra = Compra(proveedor_id=proveedor_id, usuario_id=usuario_id, actualizado_por=usuario_actual)

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


def update_compra(compra, usuario_actual):
    compra.actualizado_por = usuario_actual
    db.session.commit()


def confirmar_compra(compra_id, detalle_precios, fecha_compra, usuario_actual):
    """
    Actualiza precios de los detalles y la fecha de compra en una sola transacción.

    Args:
        compra_id: ID de la compra a confirmar
        detalle_precios: lista de tuplas (detalle_id, precio_unitario)
        fecha_compra: fecha de la compra (date)
        usuario_actual: nombre del usuario actual
    """
    compra = Compra.query.get(compra_id)
    if compra:
        compra.fecha_compra = fecha_compra
        compra.actualizado_por = usuario_actual

    for detalle_id, precio in detalle_precios:
        detalle = DetalleCompra.query.get(detalle_id)
        if detalle:
            detalle.precio_unitario = precio

    db.session.commit()


def cancelar_compra(compra_id, usuario_actual):
    compra = Compra.query.get(compra_id)
    if compra:
        compra.cancelada = True
        compra.actualizado_por = usuario_actual
        db.session.commit()
