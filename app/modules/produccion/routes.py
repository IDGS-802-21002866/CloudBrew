from flask import render_template, request, redirect, url_for, flash

from app.modules.produccion.forms import ProduccionForm
from app.modules.produccion.service import ProduccionService
from app.modules.recetas.service import RecetaService
from app.shared.decorators import verificar_rol_o_denegar
from . import bp


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin", "almacen")


produccion_service = ProduccionService()
receta_service = RecetaService()


@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "").strip()
    paginacion = produccion_service.listar_produccion(page=page, per_page=10)
    return render_template(
        "produccion/listar.html",
        pagination=paginacion,
        search_term=search_term,
    )


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


@bp.route("/terminadas")
def listar_terminadas():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "").strip()
    paginacion = produccion_service.listar_produccion_completada(page=page, per_page=10)
    return render_template(
        "produccion/listar_terminadas.html",
        pagination=paginacion,
        search_term=search_term,
    )


@bp.route("/<int:id>/cancelar", methods=["POST"])
def cancelar(id):
    try:
        produccion_service.cancelar_produccion(id)
        flash("Orden de producción cancelada exitosamente", "success")
        return redirect(url_for("produccion.detalle", id=id))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("produccion.detalle", id=id))
