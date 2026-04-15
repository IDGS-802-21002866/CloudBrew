from app.modules.usuarios.model import Usuario
from app.modules.usuarios.repository import (
    get_usuario_by_email,
    get_usuario_by_id,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
    get_usuarios,
)
from app.shared.exceptions import ValidacionNegocioException
from flask_login import current_user


class UsuarioService:

    def obtener_usuarios(self, pagina=1, por_pagina=5, querry=""):
        pag = get_usuarios(pagina, por_pagina)
        if querry:
            filtrados = [
                usuario
                for usuario in pag.items
                if querry.lower() in (usuario.nombre or "").lower()
            ]
            pag.items = filtrados
        return pag

    def obtener_usuario_por_email(self, email):
        return get_usuario_by_email(email)

    def obtener_usuario_por_id(self, id_usuario):
        return get_usuario_by_id(id_usuario)

    def crear_usuario(self, data):
        usuario = crear_usuario(data, current_user.nombre)
        # Si el nuevo usuario tiene rol cliente, crear registro en clientes
        if usuario.rol and usuario.rol.name == "cliente":
            from app.modules.clientes.model import Cliente
            from app.modules.clientes.repository import create_cliente_desde_usuario

            if not Cliente.query.filter_by(email=usuario.email).first():
                create_cliente_desde_usuario(usuario)
        return usuario

    def actualizar_usuario(self, id_usuario, data):
        usuario = get_usuario_by_id(id_usuario)
        if usuario and usuario.rol and usuario.rol.name == "cliente":
            if hasattr(data, "password") and data.password.data:
                raise ValidacionNegocioException(
                    "La contraseña de usuarios cliente no puede modificarse desde el ERP. "
                    "El usuario debe usar el portal de tienda para restablecer su contraseña."
                )
        return actualizar_usuario(id_usuario, data, current_user.nombre)

    def borrar_usuario(self, id_usuario):
        return eliminar_usuario(id_usuario, current_user.nombre)
