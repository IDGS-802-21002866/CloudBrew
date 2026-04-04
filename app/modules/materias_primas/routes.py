from flask import render_template, request, redirect, url_for, flash
from app.modules.materias_primas.form import MateriaPrimaForm
from app.modules.materias_primas.service import MateriaPrimaService
from app.modules.unidades_medida.service import UnidadMedidaService
from . import bp

servicio = MateriaPrimaService()
servicio_unidades = UnidadMedidaService()

@bp.route("/")
def listar():
    materias = servicio.listar_materias(incluir_inactivas=True) 
    return render_template("materias_primas/listar.html", materias=materias)

@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = MateriaPrimaForm()
    unidades_base = servicio_unidades.listar_unidades_medida()
    unidades_base_filtradas = [u for u in unidades_base if u.es_base]
    form.id_unidad_base.choices = [(u.id, u.nombre) for u in unidades_base_filtradas]
    
    if form.validate_on_submit():
        try:
            data = {
                "nombre": form.nombre.data,
                "descripcion": form.descripcion.data,
                "id_unidad_base": form.id_unidad_base.data,
                "stock_minimo": form.stock_minimo.data
            }
            servicio.crear_materia(data)
            flash("Materia prima creada exitosamente.", "success")
            return redirect(url_for("materias_primas.listar"))
        except ValueError as e:
            flash(str(e), "danger")
    
    return render_template("materias_primas/crear.html", form=form)

@bp.route("/<int:id>")
def detalle(id):
    try:
        materia = servicio.obtener_por_id(id)
        return render_template("materias_primas/detalle.html", materia=materia)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("materias_primas.listar"))

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        materia = servicio.obtener_por_id(id)
        form = MateriaPrimaForm(obj=materia)
        
        unidades_base = servicio_unidades.listar_unidades_medida()
        unidades_base_filtradas = [u for u in unidades_base if u.es_base]
        form.id_unidad_base.choices = [(u.id, u.nombre) for u in unidades_base_filtradas]
        
        if form.validate_on_submit():
            try:
                materia.nombre = form.nombre.data
                materia.descripcion = form.descripcion.data
                materia.id_unidad_base = form.id_unidad_base.data
                materia.stock_minimo = form.stock_minimo.data
                from app import db
                db.session.commit()
                flash("Materia prima actualizada exitosamente.", "success")
                return redirect(url_for("materias_primas.detalle", id=id))
            except ValueError as e:
                flash(str(e), "danger")
        
        return render_template("materias_primas/crear.html", form=form, materia=materia)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("materias_primas.listar"))

@bp.route("/<int:id>/desactivar", methods=["POST"])
def desactivar(id):
    try:
        servicio.desactivar_materia(id)
        flash("Materia prima desactivada.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("materias_primas.listar"))

@bp.route("/<int:id>/activar", methods=["POST"])
def activar(id):
    try:
        servicio.activar_materia(id)
        flash("Materia prima activada exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("materias_primas.listar"))
