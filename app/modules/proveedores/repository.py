from app import db
from app.modules.proveedores.model import Proveedor


def get_proveedor_by_id(proveedor_id):
    """Obtiene un proveedor por id"""
    proveedor = Proveedor.query.get(proveedor_id)
    return proveedor


def get_all_proveedores():
    """Obtiene todos los proveedores activos sin paginación"""
    proveedores = Proveedor.query.filter_by(activo=True).all()
    return proveedores

def get_paginated_proveedores(page, per_page, search_term=None):
    query = Proveedor.query.filter(Proveedor.activo.is_(True))
    if search_term:
        query = query.filter(
            Proveedor.nombre.ilike(f"%{search_term}%")
        )
    return query.order_by(Proveedor.id.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )


def create_proveedor(proveedor):
    """Crea un nuevo proveedor en la BD"""
    db.session.add(proveedor)
    db.session.commit()
    return proveedor


def update_proveedor(proveedor):
    """Actualiza un proveedor en la BD"""
    db.session.commit()
    return proveedor


def delete_proveedor(proveedor_id):
    """Soft delete: desactiva un proveedor"""
    proveedor = Proveedor.query.get(proveedor_id)
    if proveedor:
        proveedor.activo = False
        db.session.commit()
    else:
        return None
    return proveedor
