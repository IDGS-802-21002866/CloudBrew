from app import db
from app.modules.proveedores.model import Proveedor
class Service:
    def obtener_proveedores(pagina=1, por_pagina=5):
        return Proveedor.query.filter_by(activo=True)\
            .paginate(page=pagina, per_page=por_pagina, error_out=False)

    def agregar_proveedor(data):
        nuevo_proveedor = Proveedor(
            nombre=data.get("nombre"),
            telefono=data.get("telefono"),
            email=data.get("email"),
            direccion=data.get("direccion"),
            activo=True
        )

        db.session.add(nuevo_proveedor)
        db.session.commit()

        return nuevo_proveedor
    
    def modificar_proveedor(id_proveedor, data):
        proveedor = Proveedor.query.get(id_proveedor)

        if not proveedor or not proveedor.activo:
            return None

        proveedor.nombre = data.get("nombre", proveedor.nombre)
        proveedor.telefono = data.get("telefono", proveedor.telefono)
        proveedor.email = data.get("email", proveedor.email)
        proveedor.direccion = data.get("direccion", proveedor.direccion)

        db.session.commit()

        return proveedor

    def eliminar_proveedor(id_proveedor):
        proveedor = Proveedor.query.get(id_proveedor)

        if not proveedor or not proveedor.activo:
            return None

        proveedor.activo = False
        db.session.commit()

        return proveedor