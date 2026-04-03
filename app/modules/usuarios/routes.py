import re

from wtforms.validators import email
from app.modules.usuarios.model import Usuario
from flask import Flask, render_template
from flask import request
from flask import redirect, url_for
import app.modules.usuarios.form
import app.modules.usuarios.service as service
from . import bp

service=service.UsuarioService();

@bp.route("/usuarios")
def index():    
    usuarios = service.obtener_usuarios()
    return render_template("lista_usuario.html", usuarios=usuarios)
@bp.route("/usuarios/agregar")
def create():
    form=app.modules.usuarios.form.UsuarioForm()
    return render_template("insertar_usuario.html", form=form)
@bp.route("/usuarios/detalles")
def detalles():
    id = request.args.get("id")
    usuario = service.obtener_usuario_por_id(id)
    form=app.modules.usuarios.form.UsuarioFormAux(obj=usuario)
    return render_template("detalle_usuario.html", form=form, usuario=usuario)

@bp.route("/usuarios/insertar", methods=["POST"])
def insert():
    form = app.modules.usuarios.form.UsuarioForm(request.form)
    if form.validate():
        flag=service.crear_usuario(form)
        if flag:
            return redirect(url_for("usuarios.index"))
        else:
            return render_template("insertar_usuario.html", form=form)
    else:
        return render_template("insertar_usuario.html", form=form)

@bp.route("/usuarios/eliminar", methods=["POST"])
def eliminar():
    id = request.args.get("id")
    service.borrar_usuario(id)
    return redirect(url_for("usuarios.index"))

@bp.route("/usuarios/actualizar", methods=["POST"])
def modificar():
    form=app.modules.usuarios.form.UsuarioFormAux(request.form)
    if form.validate():
        id= request.args.get("id")
        service.actualizar_usuario(id, form)
    return redirect(url_for("usuarios.index"))