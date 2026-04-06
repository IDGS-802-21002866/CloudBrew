from app import db
from .model import ProcesoProductivo

def obtener_por_id(proceso_id: int):
        try:
            proceso = ProcesoProductivo.query.filter_by(id=proceso_id, activo=True).first()
            if not proceso:
                raise ValueError("Proceso productivo no encontrado")
            return proceso
        except ValueError as e:
            return e
        except Exception:
            return ValueError("Error al obtener el proceso productivo")

def obtener_paginados(page: int = 1, per_page: int = 5):
    try:
        procesos = ProcesoProductivo.query.filter_by(activo=True)\
            .paginate(page=page, per_page=per_page, error_out=False)
        return procesos
    except Exception:
        return ValueError("Error al obtener los procesos productivos")

def insertar(form):
    try:
        nuevo = ProcesoProductivo(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            activo=True
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo
    except Exception:
        db.session.rollback()
        return ValueError("Error al insertar el proceso productivo")


def modificar(proceso_id: int, form):
    try:
        proceso = ProcesoProductivo.query.filter_by(id=proceso_id, activo=True).first()
        if not proceso:
            raise ValueError("Proceso productivo no encontrado")

        proceso.nombre = form.nombre.data
        proceso.descripcion = form.descripcion.data

        db.session.commit()
        return proceso
    except ValueError as e:
        return e
    except Exception:
        db.session.rollback()
        return ValueError("Error al modificar el proceso productivo")
    
def eliminacion_logica(proceso_id: int):
    try:
        proceso = ProcesoProductivo.query.filter_by(id=proceso_id, activo=True).first()
        if not proceso:
            raise ValueError("Proceso productivo no encontrado")

        proceso.activo = False
        db.session.commit()
        return proceso
    except ValueError as e:
        return e
    except Exception:
        db.session.rollback()
        return ValueError("Error al eliminar el proceso productivo")