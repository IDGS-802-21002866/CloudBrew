from app.modules.clientes import repository
from app.modules.clientes.model import Cliente
from flask_login import current_user

class ClienteService:
    def listar_clientes(self, incluir_inactivas=True):
        clientes = repository.get_all_clientes()
        if incluir_inactivas:
            return clientes
        return [c for c in clientes if c.activo]

    def listar_paginados(self, page=1, per_page=10, search_term=None):
        return repository.get_paginated_clientes(page, per_page, search_term)

    def obtener_por_id(self, id):
        cliente = repository.get_cliente_by_id(id)
        if not cliente: raise ValueError("Cliente no encontrado.")
        return cliente

    def crear_cliente(self, data):
        email = data.get("email").strip().lower()
        if repository.get_cliente_by_email(email):
            raise ValueError(f"El email '{email}' ya está registrado.")
        
        nuevo = Cliente(
            nombres=data.get("nombres").strip().title(),
            apellidos=data.get("apellidos").strip().title(),
            email=email,
            telefono=data.get("telefono"),
            calle_numero=data.get("calle_numero").strip(),
            colonia=data.get("colonia").strip(),
            ciudad=data.get("ciudad").strip(),
            estado=data.get("estado").strip(),
            codigo_postal=data.get("codigo_postal").strip(),
            tipo=data.get("tipo"),
            usuario_id=current_user.id if current_user.is_authenticated else None,
        )
        return repository.create_cliente(nuevo)

    def actualizar_cliente(self, id, data):
        c = self.obtener_por_id(id)
        c.nombres = data.get("nombres").strip().title()
        c.apellidos = data.get("apellidos").strip().title()
        c.email = data.get("email").strip().lower()
        c.telefono = data.get("telefono")
        c.calle_numero = data.get("calle_numero").strip()
        c.colonia = data.get("colonia").strip()
        c.ciudad = data.get("ciudad").strip()
        c.estado = data.get("estado").strip()
        c.codigo_postal = data.get("codigo_postal").strip()
        c.tipo = data.get("tipo")
        c.usuario_id = current_user.id if current_user.is_authenticated else c.usuario_id
        repository.update_cliente(c)

    def eliminar_cliente(self, id):
        c = self.obtener_por_id(id)
        c.usuario_id = current_user.id if current_user.is_authenticated else c.usuario_id
        repository.deactivate_cliente(c)
        return c

    def desactivar(self, id):
        c = self.obtener_por_id(id)
        c.activo = False
        repository.update_db()

    def activar(self, id):
        c = self.obtener_por_id(id)
        c.activo = True
        repository.update_db()