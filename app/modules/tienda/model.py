from datetime import datetime, timezone

from app import db


class ReservaStock(db.Model):
    """Reserva temporal de stock al agregar un producto al carrito.

    Se descuenta del stock disponible mientras el carrito esté activo,
    y se libera automáticamente al expirar, al eliminar del carrito o
    al completar la compra.
    """

    __tablename__ = "reserva_stock"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(128), nullable=False, index=True)
    producto_venta_id = db.Column(
        db.Integer, db.ForeignKey("producto_venta.id"), nullable=False
    )
    receta_id = db.Column(db.Integer, db.ForeignKey("recetas.id"), nullable=False)
    # Packs reservados (lo que el usuario agregó al carrito)
    cantidad_packs = db.Column(db.Integer, nullable=False)
    # Unidades reales descontadas del stock de inventario (packs * unidades_por_pack)
    cantidad_unidades = db.Column(db.Float, nullable=False)
    expiry = db.Column(db.DateTime(timezone=True), nullable=False)
    creado_en = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<ReservaStock session={self.session_id} producto={self.producto_venta_id} packs={self.cantidad_packs}>"
