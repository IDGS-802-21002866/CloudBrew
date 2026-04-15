from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.modules.unidades_medida.form import UnidadMedidaForm
from app.modules.unidades_medida.service import UnidadMedidaService
from app.shared.decorators import verificar_rol_o_denegar
from . import bp


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin", "almacen")


servicio = UnidadMedidaService()


@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    pagination = servicio.listar_unidades_medida(page, per_page=10)
    return render_template("unidades_medida/listar.html", pagination=pagination)


@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = UnidadMedidaForm()
    tipos_medida = servicio.listar_tipos_medida()
    form.tipo_medida_id.choices = [(t.id, t.nombre) for t in tipos_medida]

    if form.validate_on_submit():
        try:
            servicio.crear_unidad_medida(
                form.nombre.data,
                form.abreviatura.data,
                form.tipo_medida_id.data,
                form.valor_conversion.data,
            )
            flash("Unidad de medida creada exitosamente.", "success")
            return redirect(url_for("unidades_medida.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("unidades_medida/crear.html", form=form)


@bp.route("/<int:id>")
def detalle(id):
    try:
        unidad = servicio.obtener_unidad_medida(id)
        return render_template("unidades_medida/detalle.html", unidad=unidad)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("unidades_medida.listar"))


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        unidad = servicio.obtener_unidad_medida(id)

        # Si es unidad base del sistema, no permitir editar
        if unidad.es_base_sistema:
            flash("No se pueden editar las unidades base del sistema.", "danger")
            return redirect(url_for("unidades_medida.detalle", id=id))

        form = UnidadMedidaForm(obj=unidad)
        tipos_medida = servicio.listar_tipos_medida()
        form.tipo_medida_id.choices = [(t.id, t.nombre) for t in tipos_medida]

        if form.validate_on_submit():
            try:
                servicio.actualizar_unidad_medida(
                    id,
                    form.nombre.data,
                    form.abreviatura.data,
                    form.tipo_medida_id.data,
                    form.valor_conversion.data,
                )
                flash("Unidad actualizada correctamente.", "success")
                return redirect(url_for("unidades_medida.detalle", id=id))
            except ValueError as e:
                flash(str(e), "danger")

        return render_template("unidades_medida/crear.html", form=form, unidad=unidad)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("unidades_medida.listar"))


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        unidad = servicio.obtener_unidad_medida(id)
        if unidad.es_base_sistema:
            raise ValueError("No se puede eliminar una unidad base del sistema.")
        servicio.eliminar_unidad_medida(id)
        flash("Unidad de medida eliminada.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("unidades_medida.listar"))


@bp.route("/api/unidades_por_tipo/<int:tipo_medida_id>")
def api_unidades_por_tipo(tipo_medida_id):
    try:
        unidades = servicio.listar_unidades_por_tipo(tipo_medida_id)
        return jsonify([[u.id, u.nombre] for u in unidades])
    except Exception as e:
        return jsonify({"error": str(e)}), 400
