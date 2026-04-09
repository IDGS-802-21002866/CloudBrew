from app.modules.produccion.model import ProduccionProceso
from app import db


def obtener_procesos_por_produccion_ordenados(id_produccion):
    """Obtiene todos los procesos de una producción ordenados por orden ASC"""
    try:
        return (
            ProduccionProceso.query.filter_by(id_produccion=id_produccion)
            .order_by(ProduccionProceso.orden.asc())
            .all()
        )
    except Exception:
        raise


def obtener_proceso_siguiente(id_produccion):
    """Obtiene el siguiente proceso a completar (primera orden no completada)"""
    try:
        return (
            ProduccionProceso.query.filter_by(id_produccion=id_produccion)
            .filter(ProduccionProceso.estado != "completado")
            .order_by(ProduccionProceso.orden.asc())
            .first()
        )
    except Exception:
        raise


def obtener_proceso_por_id(id_produccion_proceso):
    """Obtiene un proceso específico por ID"""
    try:
        return ProduccionProceso.query.get(id_produccion_proceso)
    except Exception:
        raise


def completar_proceso(id_produccion_proceso):
    """Marca un proceso como completado"""
    try:
        proceso = ProduccionProceso.query.get(id_produccion_proceso)
        if not proceso:
            raise ValueError("El proceso no existe.")

        proceso.estado = "completado"
        db.session.add(proceso)
        db.session.flush()

        return proceso
    except Exception:
        raise
