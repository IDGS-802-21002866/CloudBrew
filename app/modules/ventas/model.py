from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Venta(db.Model):
    __tablename__ = "venta"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    id_cliente: Mapped[int] = mapped_column(
        db.Integer, ForeignKey("clientes.id"), nullable=False
    )
    id_pedido: Mapped[int] = mapped_column(
        db.Integer, ForeignKey("pedidos.id"), nullable=True
    )
    fecha: Mapped[datetime] = mapped_column(DateTime, default=db.func.now())
    cancelada: Mapped[bool] = mapped_column(db.Boolean, default=False)
    tipo: Mapped[str] = mapped_column(db.String(20), nullable=False)
    total: Mapped[float] = mapped_column(db.Float, nullable=True)

    # Relaciones
    cliente = relationship(
        "Cliente", foreign_keys=[id_cliente], back_populates="ventas"
    )
    pedido = relationship("Pedido", foreign_keys=[id_pedido], back_populates="ventas")
    detallesVenta = relationship("DetalleVenta", back_populates="venta")


class DetalleVenta(db.Model):
    __tablename__ = "detalle_venta"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    id_venta: Mapped[int] = mapped_column(
        db.Integer, ForeignKey("venta.id"), nullable=False
    )
    id_receta: Mapped[int] = mapped_column(
        db.Integer, ForeignKey("recetas.id"), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(db.Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(db.Float, nullable=True)
    subtotal: Mapped[float] = mapped_column(db.Float, nullable=True)

    # Relaciones
    venta = relationship("Venta", back_populates="detallesVenta")
    receta = relationship("Recetas", foreign_keys=[id_receta])
