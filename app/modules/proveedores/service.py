from . import repository

class ProveedorService:
    @staticmethod
    def proveedor_by_id(id_proveedor):
        return repository.proveedor_by_id(id_proveedor)

    @staticmethod
    def obtener_proveedores(pagina=1, por_pagina=5, querry=""):
        proveedores = repository.obtener_proveedores(pagina, por_pagina)
        if querry:
            proveedores = [
                proveedor for proveedor in proveedores.items
                if querry.lower() in (proveedor.nombre or "").lower()
            ]
            return proveedores

        return proveedores

    @staticmethod
    def agregar_proveedor(data):
        return repository.agregar_proveedor(data)

    @staticmethod
    def modificar_proveedor(id_proveedor, data):
        return repository.modificar_proveedor(id_proveedor, data)

    @staticmethod
    def eliminar_proveedor(id_proveedor):
        return repository.eliminar_proveedor(id_proveedor)