import re

from wtforms.validators import email

from app.modules.proveedores.model import Proveedor
from flask import Flask, render_template
from flask import request
from flask import redirect, url_for
import app.modules.proveedores.form
import app.modules.proveedores.service as service
from . import bp

service=service.Service;

from flask import flash
@bp.route("/proveedores")
def listado():
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "", type=str)
    pag =service.obtener_proveedores(pagina=page, por_pagina=5)
    proveedores = pag.items
    if q:
        proveedores = [
            p for p in proveedores
            if q.lower() in (p.nombre or "").lower()
        ]
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
    return render_template("list.html",proveedores=proveedores,pagination=pagination)

@bp.route("/proveedores/agregar", methods=["GET", "POST"])
def agregar_proveedor():
    form=app.modules.proveedores.form.ProveedorForm()
    return render_template("insert.html",form=form)
@bp.route("/proveedores/detalles", methods=["GET", "POST"])
def detalles_proveedor():
    id = request.args.get("id", type=int)
    prov = Proveedor.query.get(id)
    form =app.modules.proveedores.form.ProveedorForm(obj=prov)
    return render_template("details.html", proveedor=prov,form=form)

@bp.route("/proveedores/eliminar", methods=["POST"])
def eliminar_proveedor():
    id = request.args.get("id", type=int)
    proveedor = service.eliminar_proveedor(id)
    if proveedor:
        flash("Proveedor eliminado correctamente", "success")
    else:
        flash("Proveedor no encontrado", "warning")
    return redirect(url_for("proveedores.listado"))

@bp.route("/proveedores/modificar", methods=["POST"])
def modificar_proveedor():
    data = request.form
    id = request.args.get("id", type=int)
    proveedor = service.modificar_proveedor(id, data)
    if proveedor:
        flash("Proveedor actualizado correctamente", "success")
    else:
        flash("Proveedor no encontrado", "warning")
    return redirect(url_for("proveedores.listado"))

@bp.route("/proveedores/insertar", methods=["POST"])
def insertar_proveedor():
    print("Datos recibidos:", request.form)
    try:
        data = request.form
        service.agregar_proveedor(data)
        flash("Proveedor agregado correctamente", "success")
    except Exception as e:
        flash(f"Error al agregar proveedor: {str(e)}", "danger")
    return redirect(url_for("proveedores.listado"))