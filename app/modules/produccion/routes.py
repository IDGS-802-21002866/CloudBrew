from flask import render_template, request, redirect, url_for, flash

from app.modules.produccion.forms import ProduccionForm
from app.modules.produccion.service import ProduccionService
from app.modules.recetas.service import RecetaService
from . import bp
from app.shared.decorators import login_required

produccion_service = ProduccionService()
receta_service = RecetaService()


@login_required
@bp.route("/")
def listar():
    producciones = produccion_service.listar_produccion()
    return render_template("produccion/listar.html", producciones=producciones)


@login_required
@bp.route("/<int:id>", methods=["GET"])
def detalle(id):
    produccion = produccion_service.buscar_produccion_por_id(id)
    if isinstance(produccion, ValueError) or not produccion:
        flash("Orden de producción no encontrada", "danger")
        return redirect(url_for("produccion.listar"))
    procesos = produccion_service.obtener_procesos_de_produccion(id)
    return render_template(
        "produccion/detalle.html", produccion=produccion, procesos=procesos
    )


@login_required
@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = ProduccionForm()
    recetas = receta_service.listar_recetas(incluir_inactivas=False)
    form.id_receta.choices = [(r.id, r.nombre) for r in recetas]
    recetas_data = {r.id: r.cantidad_producida for r in recetas}

    if form.validate_on_submit():
        try:
            produccion_service.crear_produccion(
                {
                    "id_receta": form.id_receta.data,
                    "cantidad": form.cantidad.data,
                }
            )
            flash("Orden de producción creada exitosamente", "success")
            return redirect(url_for("produccion.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "produccion/crear.html", form=form, recetas_data=recetas_data
    )


@login_required
@bp.route("/<int:id>/cancelar", methods=["POST"])
def cancelar(id):
    try:
        produccion_service.cancelar_produccion(id)
        flash("Orden de producción cancelada exitosamente", "success")
        return redirect(url_for("produccion.detalle", id=id))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("produccion.detalle", id=id))
