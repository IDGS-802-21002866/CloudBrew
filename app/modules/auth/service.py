from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

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
