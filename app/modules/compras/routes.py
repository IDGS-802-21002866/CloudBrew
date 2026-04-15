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
    ordenes_compra = compras_service.listar_ordenes_compra()
    return render_template(
        "compras/listar.html",
        solicitudes_pendientes=solicitudes_pendientes,
        ordenes_compra=ordenes_compra,
    )


@bp.route("/solicitudes/<int:solicitud_id>/atender", methods=["GET", "POST"])
def atender_solicitud(solicitud_id):
    orden_form = OrdenDeCompraForm()
    detalles_form = OrdenDeCompraDetallesForm()

    proveedores = proveedores_service.listar_proveedores()
    orden_form.proveedor_id.choices = [(p.id, p.nombre) for p in proveedores]

    solicitud = compras_service.obtener_solicitud(solicitud_id)

    # --- FILTRO CRÍTICO ---
    # Solo mostramos presentaciones que coincidan con el tipo de medida de la materia prima
    presentaciones = [
        p
        for p in presentaciones_service.listar_presentaciones(incluir_inactivas=False)
        if p.tipo_medida_id == solicitud.materia_prima.tipo_medida_id
    ]

    detalles_form.materia_prima_id.choices = [
        (solicitud.materia_prima_id, solicitud.materia_prima.nombre)
    ]
    detalles_form.presentacion_id.choices = [(p.id, p.nombre) for p in presentaciones]

    if request.method == "GET":
        detalles_form.materia_prima_id.data = solicitud.materia_prima_id
        # Sugerimos la cantidad que viene de la solicitud
        detalles_form.cantidad.data = solicitud.cantidad

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
                compra_id = compras_service.crear_compra(
                    proveedor_id=orden_form.proveedor_id.data,
                    usuario_id=current_user.id,
                    detalles=carrito,
                )
                compras_service.marcar_solicitud_estado(solicitud_id, "En Compra")
                return redirect(
                    url_for(
                        "compras.confirmar_compra",
                        id=compra_id,
                        solicitud_id=solicitud_id,
                    )
                )
            except (ValidacionNegocioException, ValueError) as e:
                flash(str(e), "danger")
        else:
            for field, errors in orden_form.errors.items():
                for error in errors:
                    flash(error, "danger")
            for field, errors in detalles_form.errors.items():
                for error in errors:
                    flash(error, "danger")

    # Lógica de cálculos para la UI
    unidades_pedidas = 0
    cantidad_producida = 0
    cantidad_ingrediente = 0
    total_materia_necesaria = solicitud.cantidad

    if solicitud.referencia and solicitud.referencia.detalles:
        # Asumimos el primer detalle del pedido ligado
        p_det = solicitud.referencia.detalles[0]
        unidades_pedidas = float(p_det.total_unidades or 0)

        if p_det.producto_venta and p_det.producto_venta.receta:
            cantidad_producida = float(
                p_det.producto_venta.receta.cantidad_producida or 1
            )
            for ing in p_det.producto_venta.receta.detalle:
                if ing.materia_prima_id == solicitud.materia_prima_id:
                    cantidad_ingrediente = float(ing.cantidad)
                    break

        if unidades_pedidas > 0 and cantidad_producida > 0:
            total_materia_necesaria = (
                unidades_pedidas / cantidad_producida
            ) * cantidad_ingrediente

    return render_template(
        "compras/atender_solicitud.html",
        solicitud=solicitud,
        form=orden_form,
        detalles_form=detalles_form,
        presentaciones=presentaciones,
        unidades_pedidas=unidades_pedidas,
        cantidad_producida=cantidad_producida,
        cantidad_ingrediente=cantidad_ingrediente,
        total_materia_necesaria=round(total_materia_necesaria, 2),
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
    solicitud_id = request.args.get("solicitud_id")
    try:
        compra = compras_service.obtener_compra(id)
    except ValidacionNegocioException as e:
        flash(str(e), "danger")
        return redirect(url_for("compras.listar"))

    if confirmacion_form.validate_on_submit():
        detalle_ids = request.form.getlist("detalle_id")
        precios = request.form.getlist("precio_unitario")
        solicitud_id = request.form.get("solicitud_id") or solicitud_id
        try:
            compras_service.confirmar_compra(
                compra_id=id,
                detalle_ids=detalle_ids,
                precios=precios,
                solicitud_id=solicitud_id,
            )
            flash("Compra confirmada exitosamente.", "success")
            return redirect(url_for("compras.detalle", id=id))
        except ValidacionNegocioException as e:
            flash(str(e), "danger")

    return render_template(
        "compras/confirmacion.html",
        compra=compra,
        form=confirmacion_form,
        solicitud_id=solicitud_id,
    )
