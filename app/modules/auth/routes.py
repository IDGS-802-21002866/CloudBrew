from flask import flash, redirect, render_template, request, url_for

from app.modules.auth import bp
from app.modules.auth.forms import LoginForm
from app.modules.auth.service import AuthService
from app.modules.usuarios.repository import getUsuarioByEmail

auth_service = AuthService()


@bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            auth_service.iniciar_sesion(form.correo.data, form.contrasenia.data)
            return redirect(url_for("main.index"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=["GET"])
def logout():
    auth_service.cerrar_sesion()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("auth.login"))
