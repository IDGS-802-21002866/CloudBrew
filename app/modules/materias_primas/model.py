from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class MateriaPrima(db.Model):
    __tablename__ = "materias_primas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=True)
    tipo_medida_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tipo_medida.id"), nullable=False
    )
    stock_minimo: Mapped[float] = mapped_column(Float, default=0.0)
    activo: Mapped[bool] = mapped_column(db.Boolean, default=True)

    # Relación para saber qué tipo de medida usa (Masa, Volumen, Pieza)
    tipo_medida = relationship("TipoMedida")

    # Relación con detalles de compra
    compras = relationship("DetalleCompra", back_populates="materia_prima")

    # Relacion con movimiento de materia prima
    movimientos = relationship(
        "MovimientosMateriaPrima", back_populates="materia_prima"
    )

    recetas_detalle = relationship("RecetaDetalle", back_populates="materia_prima")
