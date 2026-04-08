import re

from wtforms.validators import email
from app.modules.usuarios.model import Usuario
from flask import Flask, flash, render_template
from flask import request
from flask import redirect, url_for
import app.modules.usuarios.form
import app.modules.usuarios.service as service
from . import bp

service = service.UsuarioService()


@bp.route("/usuarios")
def listar():
    try:
        page = request.args.get("page", 1, type=int)
        querry = request.args.get("querry", "", type=str)
        pag = service.obtener_usuarios(pagina=page, por_pagina=5, querry=querry)
        usuarios = pag.items
        pagination = {
            "page": pag.page,
            "pages": list(range(1, pag.pages + 1)),
            "has_prev": pag.has_prev,
            "has_next": pag.has_next,
            "prev_num": pag.prev_num,
            "next_num": pag.next_num,
            "total": pag.total,
            "start": (pag.page - 1) * pag.per_page + 1 if pag.total > 0 else 0,
            "end": min(pag.page * pag.per_page, pag.total),
        }
        return render_template(
            "lista_usuario.html", usuarios=usuarios, pagination=pagination
        )

    except ValueError as e:
        flash(str(e), "danger")
        return render_template("lista_usuario.html", usuarios=[])


@bp.route("/usuarios/agregar")
def crear():
    form = app.modules.usuarios.form.UsuarioForm()
    return render_template("insertar_usuario.html", form=form)


@bp.route("/usuarios/detalles")
def detalles():
    try:
        id = request.args.get("id", type=int)

        usuario = service.obtener_usuario_por_id(id)
        form = app.modules.usuarios.form.UsuarioFormAux(obj=usuario)

        return render_template("detalle_usuario.html", form=form, usuario=usuario)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("usuarios.listar"))


@bp.route("/usuarios/insertar", methods=["POST"])
def insert():
    form = app.modules.usuarios.form.UsuarioForm(request.form)
    if form.validate():
        try:
            service.crear_usuario(form)
            flash("Usuario creado correctamente", "success")
            return redirect(url_for("usuarios.listar"))
        except ValueError as e:
            flash(str(e), "danger")
    else:
        flash("Verifique los datos ingresados", "danger")
    return render_template("insertar_usuario.html", form=form)


@bp.route("/usuarios/eliminar", methods=["POST"])
def eliminar():
    try:
        id = request.args.get("id", type=int)
        service.borrar_usuario(id)
        flash("Usuario eliminado correctamente", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("usuarios.listar"))


@bp.route("/usuarios/actualizar", methods=["POST"])
def modificar():
    form = app.modules.usuarios.form.UsuarioFormAux(request.form)
    if form.validate():
        try:
            id = request.args.get("id", type=int)
            service.actualizar_usuario(id, form)
            flash("Usuario actualizado correctamente", "success")
        except ValueError as e:
            flash(str(e), "danger")
    else:
        flash("Verifique los datos ingresados", "danger")
    return redirect(url_for("usuarios.listar"))
