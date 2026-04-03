from app import db
from app.modules.proveedores.model import Proveedor

def proveedor_by_id(id_proveedor):
    if not id_proveedor:
        raise ValueError("El 'id_proveedor' es obligatorio")
    proveedor = Proveedor.query.get(id_proveedor)
    if not proveedor:
        raise ValueError(f"No existe un proveedor con id {id_proveedor}")
    return proveedor

def obtener_proveedores(pagina=1, por_pagina=5):
    if pagina < 1 or por_pagina < 1:
        raise ValueError("Los parámetros 'pagina' y 'por_pagina' deben ser mayores a 0")
    proveedores = Proveedor.query.filter_by(activo=True)\
        .paginate(page=pagina, per_page=por_pagina, error_out=False)
    if not proveedores:
        raise ValueError("No hay proveedores activos registrados")
    return proveedores


def agregar_proveedor(data):
    if not data:
        raise ValueError("No se proporcionaron datos para crear el proveedor")

    if not data.get("nombre"):
        raise ValueError("El campo 'nombre' es obligatorio")

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
    if not id_proveedor:
        raise ValueError("El 'id_proveedor' es obligatorio")

    if not data:
        raise ValueError("No se proporcionaron datos para modificar el proveedor")

    proveedor = Proveedor.query.get(id_proveedor)

    if not proveedor:
        raise ValueError(f"No existe un proveedor con id {id_proveedor}")

    if not proveedor.activo:
        raise ValueError(f"El proveedor con id {id_proveedor} está inactivo")

    proveedor.nombre = data.get("nombre", proveedor.nombre)
    proveedor.telefono = data.get("telefono", proveedor.telefono)
    proveedor.email = data.get("email", proveedor.email)
    proveedor.direccion = data.get("direccion", proveedor.direccion)

    db.session.commit()

    return proveedor


def eliminar_proveedor(id_proveedor):
    if not id_proveedor:
        raise ValueError("El 'id_proveedor' es obligatorio")

    proveedor = Proveedor.query.get(id_proveedor)

    if not proveedor:
        raise ValueError(f"No existe un proveedor con id {id_proveedor}")

    if not proveedor.activo:
        raise ValueError(f"El proveedor con id {id_proveedor} ya está inactivo")

    proveedor.activo = False
    db.session.commit()

    return proveedor