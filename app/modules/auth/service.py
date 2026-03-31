from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from app.modules.usuarios.repository import getUsuarioByEmail


class AuthService:
    def iniciar_sesion(self, correo, contrasenia):
        usuario = getUsuarioByEmail(correo)

        if not usuario or not check_password_hash(usuario.password, contrasenia):
            raise ValueError("Credenciales incorrectas")

        login_user(usuario)

        return usuario

    def cerrar_sesion(self):
        logout_user()
