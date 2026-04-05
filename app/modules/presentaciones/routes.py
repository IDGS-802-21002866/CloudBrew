from flask import render_template, request, redirect, url_for, flash
from app.modules.presentaciones.form import PresentacionForm
from app.modules.presentaciones.service import PresentacionService
from app.modules.unidades_medida.service import UnidadMedidaService
from . import bp

servicio = PresentacionService()
servicio_unidades = UnidadMedidaService()

@bp.route("/")
def listar():
    presentaciones = servicio.listar_presentaciones(True)
    return render_template("presentaciones/listar.html", presentaciones=presentaciones)

@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = PresentacionForm()
    unidades_base = servicio_unidades.listar_unidades_medida()
    form.id_unidad.choices = [(u.id, u.nombre) for u in unidades_base if u.es_base]

    if form.validate_on_submit():
        try:
            data = {
                "nombre": form.nombre.data,
                "id_unidad": form.id_unidad.data,
                "cantidad_equivalente": form.cantidad_equivalente.data
            }
            servicio.crear_presentacion(data)
            flash("Presentación creada exitosamente.", "success")
            return redirect(url_for("presentaciones.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("presentaciones/crear.html", form=form)

@bp.route("/<int:id>")
def detalle(id):
    try:
        presentacion = servicio.obtener_por_id(id)
        return render_template("presentaciones/detalle.html", presentacion=presentacion)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("presentaciones.listar"))

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        presentacion = servicio.obtener_por_id(id)
        form = PresentacionForm(obj=presentacion)

        unidades_base = servicio_unidades.listar_unidades_medida()
        form.id_unidad.choices = [(u.id, u.nombre) for u in unidades_base if u.es_base]

        if form.validate_on_submit():
            try:
                data = {
                    "nombre": form.nombre.data,
                    "id_unidad": form.id_unidad.data,
                    "cantidad_equivalente": form.cantidad_equivalente.data
                }
                servicio.actualizar_presentacion(id, data)
                flash("Presentación actualizada exitosamente.", "success")
                return redirect(url_for("presentaciones.detalle", id=id))
            except ValueError as e:
                flash(str(e), "danger")

        return render_template("presentaciones/crear.html", form=form, presentacion=presentacion)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("presentaciones.listar"))

@bp.route("/<int:id>/desactivar", methods=["POST"])
def desactivar(id):
    try:
        servicio.desactivar(id)
        flash("Presentación desactivada exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("presentaciones.listar"))

@bp.route("/<int:id>/activar", methods=["POST"])
def activar(id):
    try:
        servicio.activar(id)
        flash("Presentación activada exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("presentaciones.listar"))
