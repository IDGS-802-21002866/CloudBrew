from flask_login import current_user
from app import db
from app.modules.mermas_materia_prima.model import MermaMateriaPrima
from app.modules.materias_primas.model import MateriaPrima


def get_all_mermas_activas():
    return (
        MermaMateriaPrima.query.filter_by(activo=True)
        .order_by(MermaMateriaPrima.fecha_registro.desc())
        .all()
    )


def get_paginated_mermas(page, per_page, search_term=None):
    query = MermaMateriaPrima.query.join(MateriaPrima)

    if search_term:
        query = query.filter(MateriaPrima.nombre.ilike(f"%{search_term}%"))

    return (
        query.order_by(MermaMateriaPrima.fecha_registro.desc())
        .paginate(page=page, per_page=per_page)
    )


def get_merma_by_id(merma_id):
    return MermaMateriaPrima.query.get(merma_id)


def save(merma):
    if current_user.is_authenticated:
        merma.actualizado_por = current_user.nombre
    db.session.add(merma)
    db.session.commit()
    return merma


def deactivate(merma):
    if current_user.is_authenticated:
        merma.actualizado_por = current_user.nombre
    merma.activo = False
    db.session.commit()
    return merma


def commit():
    db.session.commit()
