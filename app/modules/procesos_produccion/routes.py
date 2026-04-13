from flask import render_template, redirect, url_for, flash
from app.modules.procesos_produccion import bp, service
from app.shared.exceptions import ValidacionNegocioException


@bp.route("/<int:produccion_id>")
def listar(produccion_id):
    """
    Lista todos los procesos de una producción.
    Muestra cuál es el siguiente a completar.
    """
    try:
        datos = service.listar_procesos_produccion(produccion_id)
        return render_template(
            "procesos_produccion/listar.html",
            id_produccion=produccion_id,
            procesos=datos["procesos"],
            proceso_siguiente=datos["proceso_siguiente"],
            total_procesos=datos["total"],
            procesos_completados=datos["completados"],
        )
    except ValidacionNegocioException as e:
        flash(str(e), "error")
        return redirect(url_for("produccion.listar"))
    except Exception as e:
        flash(f"Error al cargar procesos: {str(e)}", "error")
        return redirect(url_for("produccion.listar"))


@bp.route("/<int:proceso_id>/completar", methods=["POST"])
def completar(proceso_id):
    """
    Marca un proceso como completado.
    Valida que sea el siguiente en la secuencia.
    """
    try:
        proceso_completado = service.completar_proceso(proceso_id)
        flash(
            f'Proceso "{proceso_completado.proceso.nombre}" completado exitosamente.',
            "success",
        )

        # Redirigir a la lista de procesos de la misma producción
        return redirect(
            url_for(
                "procesos_produccion.listar",
                produccion_id=proceso_completado.id_produccion,
            )
        )
    except ValidacionNegocioException as e:
        flash(str(e), "error")
        # Intentar obtener id_produccion del parámetro, sino redirigir a produccion
        return redirect(url_for("produccion.listar"))
    except Exception as e:
        flash(f"Error al completar el proceso: {str(e)}", "error")
        return redirect(url_for("produccion.listar"))
