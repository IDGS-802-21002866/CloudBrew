from app.modules.usuarios.model import Usuario
from app.modules.usuarios.repository import (
    getUsuarioByEmail,
    getUsuarioById,
    insertar_usuario,
    modificar_usuario,
    eliminar_usuario,
    get_usuarios
)
class UsuarioService:

    def obtener_usuarios(self, pagina=1, por_pagina=5, querry=""):
        pag = get_usuarios(pagina, por_pagina)
        if querry:
            filtrados = [
                usuario for usuario in pag.items
                if querry.lower() in (usuario.nombre or "").lower()
            ]
            pag.items = filtrados
        return pag

    def obtener_usuario_por_email(self, email):
        return getUsuarioByEmail(email)

    def obtener_usuario_por_id(self, id_usuario):
        return getUsuarioById(id_usuario)

    def crear_usuario(self, data):
        return insertar_usuario(data)

    def actualizar_usuario(self, id_usuario, data):
        return modificar_usuario(id_usuario, data)

    def borrar_usuario(self, id_usuario):
        return eliminar_usuario(id_usuario)