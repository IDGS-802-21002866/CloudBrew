from flask import render_template, request, redirect, url_for, flash
from app.modules.proveedores.form import ProveedorForm
from app.modules.proveedores.service import ProveedorService
from . import bp
from app.shared.decorators import login_required

servicio = ProveedorService()


@login_required
@bp.route("/")
def listar():
    try:
        page = request.args.get("page", 1, type=int)
        pagination = servicio.obtener_proveedores_paginados(page, per_page=5, busqueda=None)
        return render_template(
            "proveedores/listar.html",
            pagination=pagination,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("proveedores.listar"))


@login_required
@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = ProveedorForm()
    if form.validate_on_submit():
        try:
            datos = {
                "nombre": form.nombre.data,
                "telefono": form.telefono.data,
                "email": form.email.data,
                "direccion": form.direccion.data,
            }
            servicio.crear_proveedor(datos)
            flash("Proveedor creado exitosamente", "success")
            return redirect(url_for("proveedores.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("proveedores/crear.html", form=form)


@login_required
@bp.route("/<int:id>")
def detalle(id):
    try:
        proveedor = servicio.obtener_proveedor(id)
        return render_template("proveedores/detalle.html", proveedor=proveedor)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("proveedores.listar"))


@login_required
@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        proveedor = servicio.obtener_proveedor(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("proveedores.listar"))

    form = ProveedorForm(obj=proveedor)
    if form.validate_on_submit():
        try:
            datos = {
                "nombre": form.nombre.data,
                "telefono": form.telefono.data,
                "email": form.email.data,
                "direccion": form.direccion.data,
            }
            servicio.actualizar_proveedor(id, datos)
            flash("Proveedor actualizado exitosamente", "success")
            return redirect(url_for("proveedores.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("proveedores/crear.html", form=form, proveedor=proveedor)


@login_required
@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        servicio.eliminar_proveedor(id)
        flash("Proveedor eliminado exitosamente", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("proveedores.listar"))
