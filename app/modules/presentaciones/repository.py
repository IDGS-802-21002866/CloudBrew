from flask_login import current_user
from app.modules.presentaciones.model import Presentacion
from app import db

def get_all_presentaciones():
    return Presentacion.query.all()

def get_paginated_presentaciones(page, per_page, search_term=None):
    query = Presentacion.query

    if search_term:
        query = query.filter(
            Presentacion.nombre.ilike(f"%{search_term}%")
        )

    return query.order_by(Presentacion.id.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def get_presentacion_by_id(id):
    return Presentacion.query.get(id)

def get_presentacion_by_nombre(nombre):
    return Presentacion.query.filter(Presentacion.nombre == nombre).first()

def create_presentacion(presentacion):
    if current_user.is_authenticated:
        presentacion.actualizado_por = current_user.nombre
    db.session.add(presentacion)
    db.session.commit()
    return presentacion


def update_presentacion(presentacion):
    if current_user.is_authenticated:
        presentacion.actualizado_por = current_user.nombre
    db.session.commit()
    return presentacion


def deactivate_presentacion(presentacion):
    if current_user.is_authenticated:
        presentacion.actualizado_por = current_user.nombre
    presentacion.activo = False
    db.session.commit()
    return presentacion


def activate_presentacion(presentacion):
    if current_user.is_authenticated:
        presentacion.actualizado_por = current_user.nombre
    presentacion.activo = True
    db.session.commit()
    return presentacion