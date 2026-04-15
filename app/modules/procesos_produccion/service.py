from app.modules.procesos_produccion import repository
from app.modules.produccion.model import Produccion
from app.modules.compras.model import SolicitudCompra
from app.shared.exceptions import ValidacionNegocioException
from flask_login import current_user
from app import db
from datetime import date


def listar_procesos_produccion(id_produccion):
    """
    Lista todos los procesos de una producción ordenados por orden ASC.
    Incluye información de cuál es el siguiente a completar.
    """
    try:
        procesos = repository.obtener_procesos_por_produccion_ordenados(id_produccion)

        if not procesos:
            raise ValidacionNegocioException(
                "La producción no tiene procesos definidos."
            )

        # Obtener el siguiente proceso
        proceso_siguiente = repository.obtener_proceso_siguiente(id_produccion)

        return {
            "procesos": procesos,
            "proceso_siguiente": proceso_siguiente,
            "total": len(procesos),
            "completados": len([p for p in procesos if p.estado == "completado"]),
        }
    except Exception as e:
        raise


def completar_proceso(id_produccion_proceso):
    """
    Completa un proceso, validando que sea el siguiente en la secuencia.
    Si es el último, los triggers de BD crearán el lote automáticamente.
    """
    try:
        proceso = repository.obtener_proceso_por_id(id_produccion_proceso)

        if not proceso:
            raise ValidacionNegocioException("El proceso no existe.")

        if proceso.estado == "completado":
            raise ValidacionNegocioException("Este proceso ya fue completado.")

        # Validar que sea el siguiente en la secuencia
        proceso_siguiente = repository.obtener_proceso_siguiente(proceso.id_produccion)

        if (
            proceso_siguiente
            and proceso_siguiente.id_produccion_proceso != id_produccion_proceso
        ):
            raise ValidacionNegocioException(
                f"Debe completar los procesos en orden. "
                f"El siguiente es: {proceso_siguiente.proceso.nombre}"
            )

        # Completar el proceso
        proceso_completado = repository.completar_proceso(id_produccion_proceso)

        # Si es el primer proceso (orden == 1), validar compras pagadas y actualizar estado
        produccion = Produccion.query.get(proceso_completado.id_produccion)
        if proceso_completado.orden == 1 and produccion:
            # Bloquear si hay solicitudes de compra no surtidas para el pedido asociado
            if produccion.pedidos:
                for pedido_rel in produccion.pedidos:
                    if pedido_rel.pedido:
                        solicitudes = SolicitudCompra.query.filter_by(
                            referencia_id=pedido_rel.pedido.id
                        ).all()
                        no_surtidas = [s for s in solicitudes if s.estado != "Surtida"]
                        if no_surtidas:
                            raise ValidacionNegocioException(
                                "No se puede iniciar la producción. Las órdenes de compra asociadas al pedido aún no han sido surtidas."
                            )
            produccion.fecha_inicio = date.today()
            produccion.estado = "en proceso"
            db.session.add(produccion)

        # Si no hay procesos pendientes, cerrar orden de pedido retail relacionada
        siguiente_proceso = repository.obtener_proceso_siguiente(
            proceso_completado.id_produccion
        )
        if not siguiente_proceso and produccion and produccion.pedidos:
            for pedido_rel in produccion.pedidos:
                if pedido_rel.pedido and pedido_rel.pedido.estado != "Terminado":
                    # Cerrar el pedido retail vinculado cuando se completa el último proceso
                    pedido_rel.pedido.estado = "Terminado"
                    if current_user.is_authenticated:
                        pedido_rel.pedido.usuario_id = current_user.id
                    db.session.add(pedido_rel.pedido)

        db.session.commit()

        return proceso_completado
    except ValidacionNegocioException:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise ValidacionNegocioException(f"Error al completar el proceso: {str(e)}")
