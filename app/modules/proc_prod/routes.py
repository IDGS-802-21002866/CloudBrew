import re

from wtforms.validators import email
from app.modules.usuarios.model import Usuario
from flask import Flask, flash, render_template
from flask import request
from flask import redirect, url_for
from app.modules.proc_prod.form import ProcesoProductivoForm
import app.modules.proc_prod.service as service
from . import bp

service = service.ProcesoProductivoService()

@bp.route("/procprod")
def index():
    try:
        page = request.args.get("page", 1, type=int)
        querry = request.args.get("querry", "", type=str)
        pag = service.obtener_procesos(page=page, per_page=5, querry=querry)
        procprod=pag.items
        pagination = {
            "page": pag.page,
            "pages": list(range(1, pag.pages + 1)),
            "has_prev": pag.has_prev,
            "has_next": pag.has_next,
            "prev_num": pag.prev_num,
            "next_num": pag.next_num,
            "total": pag.total,
            "start": (pag.page - 1) * pag.per_page + 1 if pag.total > 0 else 0,
            "end": min(pag.page * pag.per_page, pag.total)
        }
        return render_template("lista_procprod.html", procprod=procprod,pagination=pagination)

    except ValueError as e:
        flash(str(e), "danger")
        return render_template("lista_procprod.html", procprod=[])
    
@bp.route("/procprod/agregar")
def agregar():
    form = ProcesoProductivoForm()
    return render_template("insertar_procprod.html", form=form)

@bp.route("/procprod/detalles")
def detalles():
    try:
        proceso_id = request.args.get("id", type=int)
        proceso=service.obtener_proc_por_id(proceso_id)
        form=ProcesoProductivoForm(obj=proceso)
        return render_template("detalle_procprod.html", proceso=proceso, form=form)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("procprod.index"))
    
@bp.route("/procprod/insertar", methods=["POST"])
def insertar():
    form = ProcesoProductivoForm(request.form)
    if form.validate():
        try:
            service.insertar_proc(form)
            flash("Proceso productivo insertado exitosamente", "success")
            return redirect(url_for("proc_prod.index"))
        except ValueError as e:
            flash(str(e), "danger")
    else:
        flash("Error en el formulario. Por favor, revise los campos.", "danger")
    return render_template("insertar_procprod.html", form=form)

@bp.route("/procprod/actualizar", methods=["POST"])
def modificar():    
    form = ProcesoProductivoForm(request.form)
    if form.validate():
        try:
            id = request.args.get("id", type=int)
            service.modificar_proc(id,form)
            flash("Proceso productivo actualizado exitosamente", "success")
            return redirect(url_for("proc_prod.index"))
        except ValueError as e:
            flash(str(e), "danger")
    else:
        flash("Error en el formulario. Por favor, revise los campos.", "danger")
    return render_template("detalle_procprod.html", form=form)

@bp.route("/procprod/eliminar", methods=["POST"])
def eliminar():   
    try:
        proceso_id = request.args.get("id", type=int)
        service.eliminar_proc(proceso_id)
        flash("Proceso productivo eliminado exitosamente", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("proc_prod.index"))