from flask_login import current_user
from app import db
from .model import ProcesoProductivo


def get_proceso_productivo_by_id(proceso_id: int):
    try:
        proceso = ProcesoProductivo.query.filter_by(id=proceso_id, activo=True).first()
        if not proceso:
            raise ValueError("Proceso productivo no encontrado")
        return proceso
    except ValueError as e:
        raise e
    except Exception:
        raise ValueError("Error al obtener el proceso productivo")


def get_all_procesos_productivos(page: int = 1, per_page: int = 5):
    try:
        procesos = ProcesoProductivo.query.filter_by(activo=True).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return procesos
    except Exception:
        raise ValueError("Error al obtener los procesos productivos")


def create_proceso_productivo(form, usuario_id=None):
    try:
        nuevo = ProcesoProductivo(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            activo=True,
            usuario_id=usuario_id,
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo
    except Exception:
        db.session.rollback()
        raise ValueError("Error al insertar el proceso productivo")


def update_proceso_productivo(proceso_id: int, form, usuario_id=None):
    try:
        proceso = ProcesoProductivo.query.filter_by(id=proceso_id, activo=True).first()
        if not proceso:
            raise ValueError("Proceso productivo no encontrado")

        proceso.nombre = form.nombre.data
        proceso.descripcion = form.descripcion.data
        if usuario_id is not None:
            proceso.usuario_id = usuario_id

        db.session.commit()
        return proceso
    except ValueError as e:
        raise e
    except Exception:
        db.session.rollback()
        raise ValueError("Error al modificar el proceso productivo")


def delete_proceso_productivo(proceso_id: int, usuario_id=None):
    try:
        proceso = ProcesoProductivo.query.filter_by(id=proceso_id, activo=True).first()
        if not proceso:
            raise ValueError("Proceso productivo no encontrado")

        proceso.activo = False
        if usuario_id is not None:
            proceso.usuario_id = usuario_id
        db.session.commit()
        return proceso
    except ValueError as e:
        raise e
    except Exception:
        db.session.rollback()
        raise ValueError("Error al eliminar el proceso productivo")
