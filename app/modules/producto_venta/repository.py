from app import db
from app.modules.producto_venta.model import ProductoVenta


def get_all_producto_venta():
    return ProductoVenta.query.all()


def get_producto_venta_by_id(id):
    return ProductoVenta.query.get(id)


def get_producto_venta_by_tipo(tipo):
    return ProductoVenta.query.filter_by(tipo=tipo, activo=True).all()


def get_activos_producto_venta():
    return ProductoVenta.query.filter_by(activo=True).all()


def get_productos_venta_paginados(page=1, per_page=10, search_term=None):
    """Obtiene productos paginados con búsqueda opcional."""
    from app.modules.recetas.model import Recetas

    query = ProductoVenta.query
    if search_term:
        search = f"%{search_term}%"
        query = query.filter(
            db.or_(
                ProductoVenta.nombre.ilike(search),
                ProductoVenta.receta.any(Recetas.nombre.ilike(search)),
            )
        )
    return query.paginate(page=page, per_page=per_page, error_out=False)


def create_producto_venta(producto_venta):
    db.session.add(producto_venta)
    db.session.commit()
    return producto_venta


def update_producto_venta(producto_venta):
    db.session.commit()
    return producto_venta


def delete_producto_venta(producto_venta):
    db.session.delete(producto_venta)
    db.session.commit()


def deactivate_producto_venta(producto_venta):
    producto_venta.activo = False
    db.session.commit()
    return producto_venta


def activate_producto_venta(producto_venta):
    producto_venta.activo = True
    db.session.commit()
    return producto_venta
