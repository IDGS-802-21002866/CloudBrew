from sqlalchemy import String, Integer, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from datetime import datetime

class MermaProductoTerminado(db.Model):
    __tablename__ = "mermas_producto_terminado"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    receta_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recetas.id"), nullable=False
    )
    lote_id: Mapped[int] = mapped_column(
    Integer, ForeignKey("lotes_produccion.id_lote"), nullable=True
    )
    lote = relationship("LoteProduccion")
    cantidad: Mapped[float] = mapped_column(Float, nullable=False)
    motivo: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuario.id"), nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    receta = relationship("Recetas", back_populates="mermas")
    usuario = relationship("Usuario")

    @property
    def folio(self):
        return f"MPT-{self.id:03d}"