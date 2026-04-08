import secrets
from datetime import datetime, timedelta, timezone

from flask import current_app, render_template, url_for
from flask_login import login_user, logout_user
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash

from app import mail
from app.modules.usuarios.repository import (
    get_usuario_by_reset_token,
    getUsuarioByEmail,
    guardar_token_recuperacion,
    limpiar_token_recuperacion,
    actualizar_password,
)
from app.modules.usuarios.service import UsuarioService

usuarios_service = UsuarioService()


class AuthService:
    def iniciar_sesion(self, correo, contrasenia):
        usuario = usuarios_service.obtener_usuario_por_email(correo)

        if not usuario:
            raise ValueError("Credenciales incorrectas")

        if not check_password_hash(usuario.password, contrasenia):
            raise ValueError("Credenciales incorrectas")

        login_user(usuario)

        return usuario

    def cerrar_sesion(self):
        logout_user()

    def solicitar_recuperacion(self, correo):
        usuario = getUsuarioByEmail(correo)
        if not usuario or not usuario.activo:
            raise ValueError("Correo inválido")

        token = secrets.token_urlsafe(32)
        expiry = datetime.now(timezone.utc) + timedelta(hours=1)
        guardar_token_recuperacion(usuario, token, expiry)

        enlace = url_for("auth.restablecer_contrasena", token=token, _external=True)
        msg = Message(
            subject="Recuperar contraseña - CloudBrew",
            recipients=[usuario.email],
            html=render_template("auth/correo_recuperacion.html", enlace=enlace, nombre=usuario.nombre),
        )
        mail.send(msg)

    def restablecer_contrasena(self, token, nueva_contrasenia):
        usuario = get_usuario_by_reset_token(token)
        if not usuario:
            raise ValueError("El enlace de recuperación no es válido")

        expiry = usuario.reset_token_expiry
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expiry:
            raise ValueError("El enlace de recuperación ha expirado")

        actualizar_password(usuario, generate_password_hash(nueva_contrasenia))
        limpiar_token_recuperacion(usuario)

