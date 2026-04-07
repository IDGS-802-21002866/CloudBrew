from app.modules.presentaciones.model import Presentacion
from app import db

def get_all_presentaciones():
    return Presentacion.query.all()

def get_presentacion_by_id(id):
    return Presentacion.query.get(id)

def get_presentacion_by_nombre(nombre):
    return Presentacion.query.filter(Presentacion.nombre == nombre).first()

def create_presentacion(presentacion):
    db.session.add(presentacion)
    db.session.commit()
    return presentacion

def update_db():
    db.session.commit()