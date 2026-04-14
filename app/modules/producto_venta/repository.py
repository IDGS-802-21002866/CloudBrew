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
