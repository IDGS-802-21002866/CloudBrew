from flask import flash, render_template, request, redirect, url_for
from app.modules.usuarios.form import UsuarioForm, UsuarioFormAux
from app.modules.usuarios.service import UsuarioService
from app.shared.decorators import verificar_rol_o_denegar
from app.shared.exceptions import ValidacionNegocioException
from . import bp


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin")


servicio = UsuarioService()


@bp.route("/")
def listar():
    try:
        page = request.args.get("page", 1, type=int)
        querry = request.args.get("querry", "", type=str)
        pag = servicio.obtener_usuarios(pagina=page, por_pagina=5, querry=querry)
        return render_template("usuarios/listar.html", pagination=pag)

    except ValueError as e:
        flash(str(e), "danger")
        return render_template("usuarios/listar.html", usuarios=[])


@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = UsuarioForm()

    if form.validate_on_submit():
        try:
            servicio.crear_usuario(form)
            flash("Usuario creado correctamente", "success")
            return redirect(url_for("usuarios.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("usuarios/crear.html", form=form)


@bp.route("/<int:id>")
def detalle(id):
    try:
        usuario = servicio.obtener_usuario_por_id(id)
        form = UsuarioFormAux(obj=usuario)
        return render_template("usuarios/detalle.html", form=form, usuario=usuario)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("usuarios.listar"))


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        usuario = servicio.obtener_usuario_por_id(id)
        form = UsuarioFormAux(obj=usuario)

        if form.validate_on_submit():
            try:
                servicio.actualizar_usuario(id, form)
                flash("Usuario actualizado correctamente", "success")
                return redirect(url_for("usuarios.detalle", id=id))
            except (ValueError, ValidacionNegocioException) as e:
                flash(str(e), "danger")

        return render_template("usuarios/crear.html", form=form, usuario=usuario)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("usuarios.listar"))


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        servicio.borrar_usuario(id)
        flash("Usuario eliminado correctamente", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("usuarios.listar"))
