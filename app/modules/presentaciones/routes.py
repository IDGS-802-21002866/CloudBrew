from flask import render_template, request, redirect, url_for, flash
from app.modules.presentaciones.form import PresentacionForm
from app.modules.presentaciones.service import PresentacionService
from app.modules.unidades_medida.service import UnidadMedidaService
from . import bp
from app.shared.decorators import login_required

servicio = PresentacionService()
servicio_unidades = UnidadMedidaService()
medidaServicio=UnidadMedidaService()


@login_required
@bp.route("/")
def listar():
    page=request.args.get("page", 1, type=int)
    paginacion = servicio.listar_presentaciones_paginadas(page, 10)
    return render_template("presentaciones/listar.html", pagination=paginacion)


@login_required
@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = PresentacionForm()
    tipos_medida = servicio_unidades.listar_tipos_medida()
    form.tipo_medida_id.choices = [(t.id, t.nombre) for t in tipos_medida]
    medidas = medidaServicio.listar_unidades_medida()
    form.medida.choices = [("", "Selecciona una medida")] + [
            (str(m.id), m.nombre) for m in medidas]
    medida_tipos = {str(m.id): str(m.tipo_medida_id) for m in medidas}

    if form.validate_on_submit():
        try:
            medida=medidaServicio.obtener_unidad_medida(form.medida.data)
            cantidad=form.cantidad_equivalente.data
            cantidad_cal=cantidad * medida.valor_conversion
            data = {
                "nombre": form.nombre.data,
                "tipo_medida_id": form.tipo_medida_id.data,
                "cantidad_equivalente": cantidad_cal,
            }
            servicio.crear_presentacion(data)
            flash("Presentación creada exitosamente.", "success")
            return redirect(url_for("presentaciones.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("presentaciones/crear.html", form=form, medidas=medidas,medida_tipos=medida_tipos)


@login_required
@bp.route("/<int:id>")
def detalle(id):
    try:
        presentacion = servicio.obtener_por_id(id)
        return render_template("presentaciones/detalle.html", presentacion=presentacion)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("presentaciones.listar"))


@login_required
@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        presentacion = servicio.obtener_por_id(id)
        form = PresentacionForm(obj=presentacion)

        tipos_medida = servicio_unidades.listar_tipos_medida()
        form.tipo_medida_id.choices = [(t.id, t.nombre) for t in tipos_medida]
        unidades = medidaServicio.listar_unidades_medida()
        form.medida.choices = [(u.id, u.nombre) for u in unidades]

        if form.validate_on_submit():
            try:
                data = {
                    "nombre": form.nombre.data,
                    "tipo_medida_id": form.tipo_medida_id.data,
                    "cantidad_equivalente": form.cantidad_equivalente.data,
                }
                servicio.actualizar_presentacion(id, data)
                flash("Presentación actualizada exitosamente.", "success")
                return redirect(url_for("presentaciones.detalle", id=id))
            except ValueError as e:
                flash(str(e), "danger")

        return render_template(
            "presentaciones/crear.html", form=form, presentacion=presentacion
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("presentaciones.listar"))


@login_required
@bp.route("/<int:id>/desactivar", methods=["POST"])
def desactivar(id):
    try:
        servicio.desactivar(id)
        flash("Presentación desactivada exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("presentaciones.listar"))


@login_required
@bp.route("/<int:id>/activar", methods=["POST"])
def activar(id):
    try:
        servicio.activar(id)
        flash("Presentación activada exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("presentaciones.listar"))
