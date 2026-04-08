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


@bp.route("/")
def listar():
    compras = compras_service.listar_compras()
    return render_template("compras/listar.html", compras=compras)


@bp.route("/crear", methods=["GET", "POST"])
def crear():
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

    if "compra_carrito" not in session:
        session["compra_carrito"] = []

    def _render():
        detalles_carrito = compras_service.obtener_carrito_con_detalles(
            session.get("compra_carrito", [])
        )
        return render_template(
            "compras/crear.html",
            form=orden_form,
            detalles_form=detalles_form,
            materias_primas=materias_primas,
            presentaciones=presentaciones,
            detalles_carrito=detalles_carrito,
        )

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "agregar_detalle":
            if not detalles_form.validate_on_submit():
                return _render()
            try:
                carrito = session["compra_carrito"]
                carrito = compras_service.agregar_al_carrito(
                    carrito,
                    int(detalles_form.materia_prima_id.data),
                    int(detalles_form.presentacion_id.data),
                    detalles_form.cantidad.data,
                )
                session["compra_carrito"] = carrito
                session.modified = True
                flash("Producto agregado al carrito.", "success")
            except ValidacionNegocioException as e:
                flash(str(e), "danger")
            return redirect(url_for("compras.crear"))

        elif accion == "quitar_detalle":
            try:
                idx = request.form.get("idx", type=int)
                carrito = session["compra_carrito"]
                carrito = compras_service.quitar_del_carrito(carrito, idx)
                session["compra_carrito"] = carrito
                session.modified = True
            except ValidacionNegocioException as e:
                flash(str(e), "danger")
            return redirect(url_for("compras.crear"))

        elif accion == "finalizar_compra":
            if not orden_form.validate_on_submit():
                return _render()
            try:
                carrito = session.get("compra_carrito", [])
                compras_service.crear_compra(
                    proveedor_id=orden_form.proveedor_id.data,
                    usuario_id=current_user.id,
                    detalles=carrito,
                )
                session["compra_carrito"] = []
                session.modified = True
                flash("Compra creada exitosamente.", "success")
                return redirect(url_for("compras.listar"))
            except (ValidacionNegocioException, ValueError) as e:
                flash(str(e), "danger")
            return redirect(url_for("compras.crear"))

    return _render()


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
