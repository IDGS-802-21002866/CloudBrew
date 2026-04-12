from flask import flash, redirect, render_template, request, url_for

from app import captcha
from app.modules.auth import bp
from app.modules.auth.forms import (
    LoginForm,
    RecuperarContrasenaForm,
    RestablecerContrasenaForm,
)
from app.modules.auth.service import AuthService
from app.modules.usuarios.repository import get_usuario_by_email
from app.modules.bitacora_login.service import BitacoraLoginService

auth_service = AuthService()
bitacora_service = BitacoraLoginService()


@bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST":
        nombre_usuario = form.correo.data if form.correo.data else "desconocido"
        
        # Validar captcha primero
        if not captcha.validate():
            bitacora_service.crear_bitacora_login(
                nombre_usuario=nombre_usuario,
                descripcion="Error en captación de Captcha",
                auth=False
            )
            flash("Captcha incorrecto. Por favor, intenta nuevamente.", "danger")
        elif form.validate_on_submit():
            try:
                auth_service.iniciar_sesion(form.correo.data, form.contrasenia.data)
                bitacora_service.crear_bitacora_login(
                    nombre_usuario=nombre_usuario,
                    descripcion="Login correcto",
                    auth=True
                )
                return redirect(url_for("main.index"))
            except ValueError as e:
                bitacora_service.crear_bitacora_login(
                    nombre_usuario=nombre_usuario,
                    descripcion="No autorizado",
                    auth=False
                )
                flash(str(e), "danger")
    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=["GET"])
def logout():
    auth_service.cerrar_sesion()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("auth.login"))


@bp.route("/recuperar", methods=["GET", "POST"])
def recuperar_contrasena():
    form = RecuperarContrasenaForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            auth_service.solicitar_recuperacion(form.correo.data)
            flash("Te enviamos un enlace para recuperar tu contraseña", "success")
        except ValueError:
            flash("Correo inválido", "danger")
        return redirect(url_for("auth.recuperar_contrasena"))
    return render_template("auth/recuperar_contrasena.html", form=form)


@bp.route("/restablecer/<token>", methods=["GET", "POST"])
def restablecer_contrasena(token):
    form = RestablecerContrasenaForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            auth_service.restablecer_contrasena(token, form.nueva_contrasenia.data)
            flash("Contraseña actualizada exitosamente", "success")
            return redirect(url_for("auth.login"))
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("auth.recuperar_contrasena"))
    return render_template("auth/restablecer_contrasena.html", form=form, token=token)
