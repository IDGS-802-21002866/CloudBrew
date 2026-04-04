from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.modules.unidades_medida.form import UnidadMedidaForm
from app.modules.unidades_medida.service import UnidadMedidaService
from . import bp

servicio = UnidadMedidaService()

@bp.route("/")
def listar():
    unidades = servicio.listar_unidades_medida()
    return render_template("unidades_medida/listar.html", unidades=unidades)

@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = UnidadMedidaForm()
    unidades_disponibles = servicio.listar_unidades_medida()
    form.unidad_base.choices = [(0, "--- Selecciona Base ---")] + [
    (u.id, u.nombre) for u in unidades_disponibles 
    if u.es_base and u.tipo == form.tipo.data
    ]
    if form.validate_on_submit():
        try:
            servicio.crear_unidad_medida(
                form.nombre.data,
                form.abreviatura.data,
                form.tipo.data,
                form.es_base.data,
                form.unidad_base.data if form.unidad_base.data != 0 else None,
                form.valor_conversion.data
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
        form = UnidadMedidaForm(obj=unidad)
        
        unidades_disponibles = servicio.listar_unidades_medida()
        form.unidad_base.choices = [(0, "--- Selecciona Base ---")] + [(u.id, u.nombre) for u in unidades_disponibles if u.es_base]

        if form.validate_on_submit():
            servicio.actualizar_unidad_medida(
                id,
                form.nombre.data,
                form.abreviatura.data,
                form.tipo.data,
                form.es_base.data,
                form.unidad_base.data if form.unidad_base.data != 0 else None,
                form.valor_conversion.data
            )
            flash("Unidad actualizada correctamente.", "success")
            return redirect(url_for("unidades_medida.detalle", id=id))
            
        return render_template("unidades_medida/crear.html", form=form, unidad=unidad)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("unidades_medida.listar"))

@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        servicio.eliminar_unidad_medida(id)
        flash("Unidad de medida eliminada.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("unidades_medida.listar"))

@bp.route("/api/unidades_base/<tipo>")
def api_unidades_base(tipo):
    unidades = servicio.obtener_unidades_base_por_tipo(tipo)
    return jsonify([(u.id, u.nombre) for u in unidades])