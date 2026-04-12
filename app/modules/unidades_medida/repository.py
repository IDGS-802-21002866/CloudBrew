from app.modules.unidades_medida.model import UnidadMedida, TipoMedida
from app import db


def get_all_unidad_medida():
    return UnidadMedida.query.filter_by(activo=True).all()


def get_unidad_medida_by_id(id):
    return UnidadMedida.query.get(id)


def get_unidad_medida_by_nombre(nombre):
    return UnidadMedida.query.filter(UnidadMedida.nombre == nombre).first()


def get_unidad_medida_by_abreviatura(abreviatura):
    return UnidadMedida.query.filter(UnidadMedida.abreviatura == abreviatura).first()


def get_unidades_by_tipo_medida_id(tipo_medida_id):
    return UnidadMedida.query.filter_by(tipo_medida_id=tipo_medida_id).all()


def get_all_tipo_medida():
    return TipoMedida.query.all()


def get_tipo_medida_by_id(id):
    return TipoMedida.query.get(id)


def get_tipo_medida_by_nombre(nombre):
    return TipoMedida.query.filter(TipoMedida.nombre == nombre).first()


def create_unidad_medida(unidad):
    db.session.add(unidad)
    db.session.commit()
    return unidad


def create_tipo_medida(tipo):
    db.session.add(tipo)
    db.session.commit()
    return tipo


def update_db():
    db.session.commit()

def update_unidad_medida(unidad):
    db.session.commit()

def deactivate_unidad_medida(unidad):
    unidad.activo = False
    db.session.commit()


def delete_unidad_medida(unidad):
    db.session.delete(unidad)
    db.session.commit()
