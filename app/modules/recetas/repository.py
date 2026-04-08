from app.modules.recetas.model import Recetas, RecetaDetalle, ProcesosReceta
from app import db


def get_all_recetas_activas():
    return Recetas.query.filter_by(activo=True).all()


def get_all_recetas_with_inactive():
    return Recetas.query.all()


def get_receta_by_id(id):
    return Recetas.query.get(id)


def get_receta_by_nombre(nombre):
    return Recetas.query.filter(Recetas.nombre == nombre).first()


def create_receta(receta):
    db.session.add(receta)
    db.session.commit()
    return receta


def update_db():
    db.session.commit()


def create_receta_detalle(detalle):
    db.session.add(detalle)
    db.session.commit()
    return detalle


def delete_receta_detalle(id):
    detalle = RecetaDetalle.query.get(id)
    if detalle:
        db.session.delete(detalle)
        db.session.commit()
    return detalle


def get_receta_detalle_by_id(id):
    return RecetaDetalle.query.get(id)


def create_proceso_receta(proceso):
    db.session.add(proceso)
    db.session.commit()
    return proceso


def delete_proceso_receta(id):
    proceso = ProcesosReceta.query.get(id)
    if proceso:
        db.session.delete(proceso)
        db.session.commit()
    return proceso


def get_proceso_receta_by_id(id):
    return ProcesosReceta.query.get(id)
