from flask import flash, render_template, request, redirect, url_for
from app.modules.usuarios.form import UsuarioForm, UsuarioFormAux
from app.modules.usuarios.service import UsuarioService
from . import bp
from app.shared.decorators import login_required

servicio = UsuarioService()


@login_required
@bp.route("/")
def listar():
    try:
        page = request.args.get("page", 1, type=int)
        querry = request.args.get("querry", "", type=str)
        pag = servicio.obtener_usuarios(pagina=page, por_pagina=5, querry=querry)
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
            "usuarios/listar.html", usuarios=usuarios, pagination=pagination
        )

    except ValueError as e:
        flash(str(e), "danger")
        return render_template("usuarios/listar.html", usuarios=[])


@login_required
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


@login_required
@bp.route("/<int:id>")
def detalle(id):
    try:
        usuario = servicio.obtener_usuario_por_id(id)
        form = UsuarioFormAux(obj=usuario)
        return render_template("usuarios/detalle.html", form=form, usuario=usuario)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("usuarios.listar"))


@login_required
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
            except ValueError as e:
                flash(str(e), "danger")

        return render_template("usuarios/crear.html", form=form, usuario=usuario)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("usuarios.listar"))


@login_required
@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        servicio.borrar_usuario(id)
        flash("Usuario eliminado correctamente", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("usuarios.listar"))
