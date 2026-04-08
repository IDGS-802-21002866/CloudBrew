from sqlalchemy import String, Integer, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = "pedidos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey('clientes.id'), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # Estados: 'Pendiente', 'En Proceso', 'Terminado', 'Cancelado'
    estado: Mapped[str] = mapped_column(String(50), default='Pendiente')
    activo: Mapped[bool] = mapped_column(db.Boolean, default=True)

    cliente = relationship("Cliente")
    detalles = relationship("PedidoDetalle", back_populates="pedido", cascade="all, delete-orphan")

    @property
    def folio(self):
        return f"PED-{self.id:04d}"

class PedidoDetalle(db.Model):
    __tablename__ = "pedido_detalle"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pedido_id: Mapped[int] = mapped_column(Integer, ForeignKey('pedidos.id'), nullable=False)
    receta_id: Mapped[int] = mapped_column(Integer, ForeignKey('recetas.id'), nullable=False)
    cantidad_lotes: Mapped[int] = mapped_column(Integer, nullable=False)
    total_unidades: Mapped[float] = mapped_column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="detalles")
    receta = relationship("Recetas")