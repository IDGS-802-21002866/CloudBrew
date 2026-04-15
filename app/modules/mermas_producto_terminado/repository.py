from app import db
from app.modules.mermas_producto_terminado.model import MermaProductoTerminado
from app.modules.recetas.model import Recetas


def get_paginated_mermas(page, per_page, search_term=None):
    query = MermaProductoTerminado.query.join(Recetas)

    if search_term:
        query = query.filter(Recetas.nombre.ilike(f"%{search_term}%"))

    return query.order_by(MermaProductoTerminado.fecha_registro.desc()).paginate(
        page=page, per_page=per_page
    )


def get_merma_by_id(merma_id):
    return MermaProductoTerminado.query.get(merma_id)


def save(merma):
    try:
        db.session.add(merma)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error al guardar la merma"+str(e))


def commit():
    db.session.commit()
