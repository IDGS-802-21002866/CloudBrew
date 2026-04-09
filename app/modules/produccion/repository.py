from app.modules.produccion.model import Produccion, ProduccionProceso
from app import db

def insertar_produccion(form):
    try:
        if not form.id_receta.data:
            raise ValueError("La receta es obligatoria.")

        produccion = Produccion(
            id_receta=form.id_receta.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            estado=form.estado.data or "pendiente"
        )

        db.session.add(produccion)
        db.session.commit()

        return produccion

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrió un error al insertar la producción.")
def modificar_produccion(id_produccion, form):
    try:
        produccion = Produccion.query.get(id_produccion)

        if not produccion:
            raise ValueError("La producción no existe.")

        produccion.id_receta = form.id_receta.data
        produccion.fecha_inicio = form.fecha_inicio.data
        produccion.fecha_fin = form.fecha_fin.data
        produccion.estado = form.estado.data

        db.session.commit()

        return produccion

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrió un error al modificar la producción.")
def eliminar_produccion(id_produccion):
    try:
        produccion = Produccion.query.get(id_produccion)

        if not produccion:
            raise ValueError("La producción no existe.")

        produccion.estado = "cancelado"

        db.session.commit()

        return produccion

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrió un error al cancelar la producción.")
def insertar_produccion_proceso(id_produccion, form):
    try:
        produccion = Produccion.query.get(id_produccion)

        if not produccion:
            raise ValueError("La producción no existe.")

        if not form.id_proceso.data:
            raise ValueError("El proceso es obligatorio.")

        proceso = ProduccionProceso(
            id_produccion=id_produccion,
            id_proceso=form.id_proceso.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            estado=form.estado.data or "pendiente"
        )

        db.session.add(proceso)
        db.session.commit()

        return proceso

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrió un error al agregar el proceso.")
def modificar_produccion_proceso(id_produccion_proceso, form):
    try:
        proceso = ProduccionProceso.query.get(id_produccion_proceso)

        if not proceso:
            raise ValueError("El proceso de producción no existe.")

        proceso.id_proceso = form.id_proceso.data
        proceso.fecha_inicio = form.fecha_inicio.data
        proceso.fecha_fin = form.fecha_fin.data
        proceso.estado = form.estado.data

        db.session.commit()

        return proceso

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrió un error al modificar el proceso.")
def eliminar_produccion_proceso(id_produccion_proceso):
    try:
        proceso = ProduccionProceso.query.get(id_produccion_proceso)

        if not proceso:
            raise ValueError("El proceso de producción no existe.")

        proceso.estado = "cancelado"

        db.session.commit()

        return proceso

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrió un error al cancelar el proceso.")

def get_procesos_por_produccion(id_produccion):
    try:
           return ProduccionProceso.query.filter_by(id_produccion=id_produccion)
    except Exception:
            return ValueError("Ocurrió un error al obtener los Procesos de producción.")
def get_produccion():
    try:
        return Produccion.query.all()
    except Exception:
            return ValueError("Ocurrió un error al obtener los registros de producción.")
def get_produccion_by_id(id):
    try:
           return Produccion.query.filter_by(id_produccion=id)
    except Exception:
            return ValueError("Ocurrió un error al obtener los registros de producción.")