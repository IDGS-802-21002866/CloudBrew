from app import db
from app.modules.ventas.model import Venta, DetalleVenta


class VentaRepository:
    def get_all_ventas(self):
        return Venta.query.order_by(Venta.fecha.desc()).all()

    def get_venta_by_id(self, id_venta):
        return Venta.query.get(id_venta)

    def update_venta(self, id_venta, **kwargs):
        venta = Venta.query.get(id_venta)
        if venta:
            for key, value in kwargs.items():
                if hasattr(venta, key):
                    setattr(venta, key, value)
            db.session.commit()
        return venta

    def get_detalles_venta(self, id_venta):
        return DetalleVenta.query.filter_by(id_venta=id_venta).all()
