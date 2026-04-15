from flask import render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from app.modules.compras import bp
from app.modules.compras.service import ComprasService
from app.modules.compras.form import (
    OrdenDeCompraConfirmacionForm,
    OrdenDeCompraForm,
    OrdenDeCompraDetallesForm,
)
from app.modules.proveedores.service import ProveedorService
from app.modules.materias_primas.service import MateriaPrimaService
from app.modules.presentaciones.service import PresentacionService
from app.shared.exceptions import ValidacionNegocioException


compras_service = ComprasService()
proveedores_service = ProveedorService()
materias_primas_service = MateriaPrimaService()
presentaciones_service = PresentacionService()


@bp.route("/", methods=["GET"])
def listar():
    solicitudes_pendientes = compras_service.listar_solicitudes_pendientes()
    compras_confirmadas = compras_service.listar_compras_confirmadas()
    return render_template(
        "compras/listar.html",
        solicitudes_pendientes=solicitudes_pendientes,
        compras_confirmadas=compras_confirmadas,
    )


@bp.route("/solicitudes/<int:solicitud_id>/atender", methods=["GET", "POST"])
def atender_solicitud(solicitud_id):
    orden_form = OrdenDeCompraForm()
    detalles_form = OrdenDeCompraDetallesForm()

    proveedores = proveedores_service.listar_proveedores()
    orden_form.proveedor_id.choices = [(p.id, p.nombre) for p in proveedores]

    materias_primas = materias_primas_service.listar_materias(incluir_inactivas=False)
    presentaciones = presentaciones_service.listar_presentaciones(
        incluir_inactivas=False
    )

    detalles_form.materia_prima_id.choices = [("", "--- Materia Prima ---")] + [
        (mp.id, mp.nombre) for mp in materias_primas
    ]
    detalles_form.presentacion_id.choices = [("", "--- Presentación ---")] + [
        (p.id, p.nombre) for p in presentaciones
    ]

    solicitud = compras_service.obtener_solicitud(solicitud_id)

    if request.method == "GET":
        detalles_form.materia_prima_id.data = solicitud.materia_prima_id
        detalles_form.cantidad.data = int(solicitud.cantidad or 0)

    if request.method == "POST":
        if orden_form.validate_on_submit() and detalles_form.validate_on_submit():
            try:
                carrito = [
                    {
                        "materia_prima_id": detalles_form.materia_prima_id.data,
                        "presentacion_id": detalles_form.presentacion_id.data,
                        "cantidad": detalles_form.cantidad.data,
                    }
                ]
                compras_service.crear_compra(
                    proveedor_id=orden_form.proveedor_id.data,
                    usuario_id=current_user.id,
                    detalles=carrito,
                )
                compras_service.marcar_solicitud_estado(solicitud_id, "En Compra")
                flash("Compra creada desde solicitud exitosamente.", "success")
                return redirect(url_for("compras.listar"))
            except (ValidacionNegocioException, ValueError) as e:
                flash(str(e), "danger")

    return render_template(
        "compras/atender_solicitud.html",
        solicitud=solicitud,
        form=orden_form,
        detalles_form=detalles_form,
        proveedores=proveedores,
        materias_primas=materias_primas,
        presentaciones=presentaciones,
    )


@bp.route("/crear")
def crear():
    return redirect(url_for("compras.listar"))


@bp.route("/<int:id>/detalle")
def detalle(id):
    try:
        compra = compras_service.obtener_compra(id)
    except ValidacionNegocioException as e:
        flash(str(e), "danger")
        return redirect(url_for("compras.listar"))

    if compra.cancelada:
        flash("No se puede ver el detalle de una compra cancelada.", "danger")
        return redirect(url_for("compras.listar"))

    return render_template("compras/detalle.html", compra=compra)


@bp.route("/<int:id>/cancelar", methods=["GET", "POST"])
def cancelar(id):
    cancelacion_form = OrdenDeCompraConfirmacionForm()
    try:
        compra = compras_service.obtener_compra(id)
    except ValidacionNegocioException as e:
        flash(str(e), "danger")
        return redirect(url_for("compras.listar"))

    if cancelacion_form.validate_on_submit():
        try:
            compras_service.cancelar_compra(id)
            flash("Compra cancelada exitosamente.", "success")
            return redirect(url_for("compras.listar"))
        except ValidacionNegocioException as e:
            flash(str(e), "danger")

    return render_template(
        "compras/cancelacion.html", compra=compra, form=cancelacion_form
    )


@bp.route("/<int:id>/confirmar_compra", methods=["GET", "POST"])
def confirmar_compra(id):
    confirmacion_form = OrdenDeCompraConfirmacionForm()
    try:
        compra = compras_service.obtener_compra(id)
    except ValidacionNegocioException as e:
        flash(str(e), "danger")
        return redirect(url_for("compras.listar"))

    if confirmacion_form.validate_on_submit():
        detalle_ids = request.form.getlist("detalle_id")
        precios = request.form.getlist("precio_unitario")
        try:
            compras_service.confirmar_compra(
                compra_id=id,
                detalle_ids=detalle_ids,
                precios=precios,
            )
            flash("Compra confirmada exitosamente.", "success")
            return redirect(url_for("compras.detalle", id=id))
        except ValidacionNegocioException as e:
            flash(str(e), "danger")

    return render_template(
        "compras/confirmacion.html", compra=compra, form=confirmacion_form
    )
