from sqlalchemy import String, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from datetime import datetime


class MermaMateriaPrima(db.Model):
    __tablename__ = "mermas_materia_prima"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    materia_prima_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("materias_primas.id"), nullable=False
    )
    cantidad: Mapped[float] = mapped_column(Float, nullable=False)
    motivo: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    usuario_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    materia_prima = relationship("MateriaPrima")
    usuario = relationship("Usuario")
    movimientos_materia_prima = relationship(
        "MovimientosMateriaPrima", back_populates="merma_materia_prima"
    )

    @property
    def folio(self):
        return f"M-{self.id:03d}"
