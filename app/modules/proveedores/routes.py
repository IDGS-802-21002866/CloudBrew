import re

from wtforms.validators import email

from app.modules.proveedores.model import Proveedor
from flask import Flask, render_template
from flask import request
from flask import redirect, url_for
import app.modules.proveedores.form
import app.modules.proveedores.service as service
from . import bp

service=service.ProveedorService;

from flask import flash
@bp.route("/proveedores")
def listado():
    try:
        page = request.args.get("page", 1, type=int)
        querry = request.args.get("querry", "", type=str)
        pag = service.obtener_proveedores(pagina=page,por_pagina=5,querry=querry)
        proveedores = pag.items
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

        return render_template("lista_proveedor.html",proveedores=proveedores,pagination=pagination)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("proveedores.listado"))
    
@bp.route("/proveedores/agregar", methods=["GET", "POST"])
def agregar_proveedor():
    form=app.modules.proveedores.form.ProveedorForm()
    return render_template("insertar_proveedor.html",form=form)

@bp.route("/proveedores/detalles", methods=["GET", "POST"])
def detalles_proveedor():
    id = request.args.get("id", type=int)
    prov = service.proveedor_by_id(id)
    form =app.modules.proveedores.form.ProveedorForm(obj=prov)
    return render_template("detalle_proveedor.html", proveedor=prov,form=form)

@bp.route("/proveedores/eliminar", methods=["POST"])
def eliminar_proveedor():
    try:
        id = request.args.get("id", type=int)
        service.eliminar_proveedor(id)
        flash("Proveedor eliminado correctamente", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("proveedores.listado"))

@bp.route("/proveedores/modificar", methods=["POST"])
def modificar_proveedor():
    try:
        id = request.args.get("id", type=int)
        form = app.modules.proveedores.form.ProveedorForm(request.form)
        if form.validate():
            service.modificar_proveedor(id, request.form)
            flash("Proveedor actualizado correctamente", "success")
        else:
            flash("Verifique los datos ingresados", "danger")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("proveedores.listado"))

@bp.route("/proveedores/insertar", methods=["POST"])
def insertar_proveedor():
    try:
        form = app.modules.proveedores.form.ProveedorForm(request.form)
        if form.validate():
            service.agregar_proveedor(request.form)
            flash("Proveedor agregado correctamente", "success")
        else:
            flash("Verifique los datos ingresados", "danger")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("proveedores.listado"))