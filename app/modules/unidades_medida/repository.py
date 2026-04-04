from app.modules.unidades_medida.model import UnidadMedida
from app import db

def get_all_unidad_medida():
    return UnidadMedida.query.all()

def get_unidad_medida_by_id(id):
    return UnidadMedida.query.get(id)

def get_unidad_medida_by_nombre(nombre):
    return UnidadMedida.query.filter(UnidadMedida.nombre == nombre).first()

def get_unidad_medida_by_abreviatura(abreviatura):
    return UnidadMedida.query.filter(UnidadMedida.abreviatura == abreviatura).first()

def get_unidades_base_por_tipo(tipo):
    return UnidadMedida.query.filter_by(tipo=tipo, es_base=True).all()

def create_unidad_medida(unidad):
    db.session.add(unidad)
    db.session.commit()
    return unidad

def update_db():
    db.session.commit()

def delete_unidad_medida(unidad):
    db.session.delete(unidad)
    db.session.commit()