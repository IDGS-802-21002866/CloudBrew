from flask import flash, redirect, render_template, request, url_for

from app.modules.presentaciones.service import PresentacionService
from app.modules.producto_venta import bp
from app.modules.producto_venta.forms import ProductoVentaForm
from app.modules.producto_venta.service import ProductoVentaService
from app.modules.recetas.service import RecetaService
from app.shared.exceptions import ValidacionNegocioException

servicio = ProductoVentaService()
receta_service = RecetaService()
presentacion_service = PresentacionService()


def _poblar_choices(form):
    recetas = receta_service.listar_recetas(incluir_inactivas=False)
    presentaciones = [
        p
        for p in presentacion_service.listar_presentaciones(incluir_inactivas=False)
        if p.uso == "comercial"
    ]
    form.receta_id.choices = [(r.id, r.nombre) for r in recetas]
    form.presentacion_id.choices = [(p.id, p.nombre) for p in presentaciones]
    return presentaciones


@bp.route("/")
def listar():
    productos = servicio.listar_productos_venta()
    return render_template("producto_venta/listar.html", productos=productos)


@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = ProductoVentaForm()
    presentaciones = _poblar_choices(form)

    if form.validate_on_submit():
        try:
            data = {
                "receta_id": form.receta_id.data,
                "presentacion_id": form.presentacion_id.data,
                "nombre": form.nombre.data,
                "descripcion": form.descripcion.data,
                "tipo": form.tipo.data,
                "precio_venta": form.precio_venta.data,
            }
            servicio.crear_producto_venta(data)
            flash("Producto de venta creado exitosamente.", "success")
            return redirect(url_for("producto_venta.listar"))
        except (ValidacionNegocioException, ValueError) as e:
            flash(str(e), "danger")

    presentaciones_map = {p.id: p.cantidad_equivalente for p in presentaciones}
    return render_template(
        "producto_venta/crear.html",
        form=form,
        presentaciones_map=presentaciones_map,
    )


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        producto = servicio.obtener_producto_venta(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("producto_venta.listar"))

    form = ProductoVentaForm(obj=producto)
    presentaciones = _poblar_choices(form)

    if form.validate_on_submit():
        try:
            data = {
                "receta_id": form.receta_id.data,
                "presentacion_id": form.presentacion_id.data,
                "nombre": form.nombre.data,
                "descripcion": form.descripcion.data,
                "tipo": form.tipo.data,
                "precio_venta": form.precio_venta.data,
            }
            servicio.actualizar_producto_venta(id, data)
            flash("Producto de venta actualizado exitosamente.", "success")
            return redirect(url_for("producto_venta.listar"))
        except (ValidacionNegocioException, ValueError) as e:
            flash(str(e), "danger")

    presentaciones_map = {p.id: p.cantidad_equivalente for p in presentaciones}
    return render_template(
        "producto_venta/editar.html",
        form=form,
        producto=producto,
        presentaciones_map=presentaciones_map,
    )


@bp.route("/<int:id>/desactivar", methods=["POST"])
def desactivar(id):
    try:
        servicio.desactivar_producto_venta(id)
        flash("Producto desactivado.", "success")
    except (ValidacionNegocioException, ValueError) as e:
        flash(str(e), "danger")
    return redirect(url_for("producto_venta.listar"))


@bp.route("/<int:id>/activar", methods=["POST"])
def activar(id):
    try:
        servicio.activar_producto_venta(id)
        flash("Producto activado.", "success")
    except (ValidacionNegocioException, ValueError) as e:
        flash(str(e), "danger")
    return redirect(url_for("producto_venta.listar"))
