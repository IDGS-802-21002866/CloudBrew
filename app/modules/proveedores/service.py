from app.modules.proveedores import repository
from app.modules.proveedores.model import Proveedor


class ProveedorService:
    def obtener_proveedor(self, id):
        proveedor = repository.get_proveedor_by_id(id)
        if not proveedor:
            raise ValueError(f"No existe un proveedor con id {id}")
        if not proveedor.activo:
            raise ValueError(f"El proveedor con id {id} está inactivo")
        return proveedor

    def listar_proveedores(self, busqueda=""):
        """Lista todos los proveedores activos con filtro de búsqueda opcional"""
        proveedores = repository.get_all_proveedores()
        if busqueda:
            proveedores = [
                p for p in proveedores if busqueda.lower() in (p.nombre or "").lower()
            ]

        return proveedores

    def crear_proveedor(self, datos):
        """Crea un nuevo proveedor después de validar datos"""
        if not datos.get("nombre"):
            raise ValueError("El nombre es obligatorio")

        nombre = datos.get("nombre").strip()
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        proveedor = Proveedor(
            nombre=nombre,
            telefono=datos.get("telefono"),
            email=datos.get("email"),
            direccion=datos.get("direccion"),
            activo=True,
        )

        return repository.create_proveedor(proveedor)

    def actualizar_proveedor(self, id, datos):
        proveedor = repository.get_proveedor_by_id(id)
        if not proveedor:
            raise ValueError(f"No existe un proveedor con id {id}")
        if not proveedor.activo:
            raise ValueError(f"El proveedor está inactivo")

        if not datos.get("nombre"):
            raise ValueError("El nombre es obligatorio")

        nombre = datos.get("nombre").strip()
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        # Actualizar
        proveedor.nombre = nombre
        proveedor.telefono = datos.get("telefono")
        proveedor.email = datos.get("email")
        proveedor.direccion = datos.get("direccion")

        return repository.update_proveedor(proveedor)

    def eliminar_proveedor(self, id):
        """Elimina (soft delete) un proveedor"""
        proveedor = repository.get_proveedor_by_id(id)
        if not proveedor:
            raise ValueError(f"No existe un proveedor con id {id}")
        if not proveedor.activo:
            raise ValueError(f"El proveedor ya está inactivo")

        return repository.delete_proveedor(id)
