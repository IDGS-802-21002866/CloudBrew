from app.modules.produccion.model import Produccion, ProduccionProceso
from app import db


def insertar_produccion(id_receta, cantidad, usuario_id=None):
    try:
        produccion = Produccion(
            id_receta=id_receta,
            cantidad=cantidad,
            estado="pendiente",
            usuario_id=usuario_id,
        )

        db.session.add(produccion)
        db.session.flush()

        return produccion

    except Exception:
        raise


def modificar_produccion(id_produccion, id_receta, cantidad, estado, usuario_id=None):
    try:
        produccion = Produccion.query.get(id_produccion)

        if not produccion:
            raise ValueError("La produccion no existe.")

        produccion.id_receta = id_receta
        produccion.cantidad = cantidad
        produccion.estado = estado
        if usuario_id is not None:
            produccion.usuario_id = usuario_id

        db.session.commit()

        return produccion

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrio un error al modificar la produccion.")


def eliminar_produccion(id_produccion, usuario_id=None):
    try:
        produccion = Produccion.query.get(id_produccion)

        if not produccion:
            raise ValueError("La produccion no existe.")

        produccion.estado = "cancelado"
        if usuario_id is not None:
            produccion.usuario_id = usuario_id

        db.session.commit()

        return produccion

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrio un error al cancelar la produccion.")


def insertar_produccion_proceso(
    id_produccion, id_proceso, orden=0, tiempo_estimado=None
):
    try:
        proceso = ProduccionProceso(
            id_produccion=id_produccion,
            id_proceso=id_proceso,
            estado="pendiente",
            orden=orden,
            tiempo_estimado=tiempo_estimado,
        )

        db.session.add(proceso)

        return proceso

    except Exception:
        raise


def modificar_produccion_proceso(id_produccion_proceso, id_proceso, estado):
    try:
        proceso = ProduccionProceso.query.get(id_produccion_proceso)

        if not proceso:
            raise ValueError("El proceso de produccion no existe.")

        proceso.id_proceso = id_proceso
        proceso.estado = estado

        db.session.commit()

        return proceso

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrio un error al modificar el proceso.")


def eliminar_produccion_proceso(id_produccion_proceso):
    try:
        proceso = ProduccionProceso.query.get(id_produccion_proceso)

        if not proceso:
            raise ValueError("El proceso de produccion no existe.")

        proceso.estado = "cancelado"

        db.session.commit()

        return proceso

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrio un error al cancelar el proceso.")


def get_procesos_por_produccion(id_produccion):
    try:
        return ProduccionProceso.query.filter_by(id_produccion=id_produccion).all()
    except Exception:
        return ValueError("Ocurrio un error al obtener los Procesos de produccion.")


def get_produccion():
    try:
        return Produccion.query.all()
    except Exception:
        return ValueError("Ocurrio un error al obtener los registros de produccion.")


def get_produccion_by_id(id):
    try:
        return Produccion.query.filter_by(id_produccion=id).first()
    except Exception:
        return ValueError("Ocurrio un error al obtener los registros de produccion.")


def get_pedido_produccion_por_produccion(id_produccion):
    from app.modules.sol_prod.model import PedidoProduccion

    return PedidoProduccion.query.filter_by(id_produccion=id_produccion).first()
