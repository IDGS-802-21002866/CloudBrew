from flask_login import current_user
from app.modules.materias_primas.model import MateriaPrima
from app import db

def get_all_materias_primas_activas():
    return MateriaPrima.query.filter_by(activo=True).all()

def get_all_materias_primas_with_inactive():
    return MateriaPrima.query.all()

def get_materia_prima_by_id(id):
    return MateriaPrima.query.get(id)

def get_materia_prima_by_nombre(nombre):
    return MateriaPrima.query.filter(MateriaPrima.nombre == nombre).first()

def create_materia_prima(materia):
    db.session.add(materia)
    db.session.commit()
    return materia


def update_materia_prima(materia):
    db.session.commit()
    return materia


def deactivate_materia_prima(materia):
    materia.activo = False
    db.session.commit()
    return materia


def activate_materia_prima(materia):
    materia.activo = True
    db.session.commit()
    return materia

def get_materias_primas(page=None, per_page=None, search_term=None, incluir_inactivas=False):
    query = MateriaPrima.query

    if not incluir_inactivas:
        query = query.filter(MateriaPrima.activo.is_(True))

    if search_term:
        query = query.filter(
            MateriaPrima.nombre.ilike(f"%{search_term}%")
        )

    query = query.order_by(MateriaPrima.id.desc())

    if page and per_page:
        return query.paginate(page=page, per_page=per_page, error_out=False)

    return query.all()


def update_db():
    db.session.commit()