from flask import render_template, request, redirect, url_for, flash

from app import db
from app.modules.produccion.forms import ProduccionForm
from app.modules.produccion.service import ProduccionService
from app.modules.recetas.service import RecetaService
from app.modules.compras.service import ComprasService
from app.modules.pedidos import repository as pedido_repo
from app.shared.exceptions import ValidacionNegocioException
from . import bp

produccion_service = ProduccionService()
receta_service = RecetaService()
compras_service = ComprasService()


@bp.route("/")
def listar():
    producciones = produccion_service.listar_produccion()
    solicitudes = compras_service.listar_solicitudes_surtidas_retail()
    return render_template(
        "produccion/listar.html",
        producciones=producciones,
        solicitudes=solicitudes,
    )


@bp.route("/solicitudes/<int:solicitud_id>/atender", methods=["GET", "POST"])
def atender_solicitud(solicitud_id):
    try:
        solicitud = compras_service.obtener_solicitud(solicitud_id)
    except ValidacionNegocioException as e:
        flash(str(e), "danger")
        return redirect(url_for("produccion.listar"))

    if solicitud.estado != "Surtida":
        flash("Solo las solicitudes surtidas pueden atenderse en producción.", "warning")
        return redirect(url_for("produccion.listar"))

    if request.method == "POST":
        if not solicitud.referencia or not solicitud.referencia.detalles:
            flash("No se encontró el pedido retail asociado para crear la producción.", "danger")
            return redirect(url_for("produccion.listar"))

        detalle_pedido = solicitud.referencia.detalles[0]
        if not detalle_pedido.receta_id or not detalle_pedido.cantidad_lotes:
            flash("La referencia del pedido no tiene datos de receta válidos.", "danger")
            return redirect(url_for("produccion.listar"))

        try:
            produccion = produccion_service.crear_produccion(
                {
                    "id_receta": detalle_pedido.receta_id,
                    "cantidad": detalle_pedido.cantidad_lotes,
                    "es_retail": True,
                    "id_solicitud_compra": solicitud.id,
                }
            )
            if solicitud.referencia:
                pedido_repo.create_pedido_produccion(
                    solicitud.referencia.id, produccion.id_produccion
                )
                db.session.commit()
            compras_service.marcar_solicitud_estado(solicitud_id, "En Proceso")
            flash("Solicitud de producción atendida y orden creada.", "success")
            return redirect(url_for("produccion.listar"))
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for("produccion.listar"))

    return render_template("produccion/atender_solicitud.html", solicitud=solicitud)


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


@bp.route("/<int:id>/cancelar", methods=["POST"])
def cancelar(id):
    try:
        produccion_service.cancelar_produccion(id)
        flash("Orden de producción cancelada exitosamente", "success")
        return redirect(url_for("produccion.detalle", id=id))
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("produccion.detalle", id=id))
