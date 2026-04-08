import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app import db


class MovimientosMateriaPrima(db.Model):
    __tablename__ = "movimientos_materia_prima"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    materia_prima_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("materias_primas.id"), nullable=False
    )
    tipo: Mapped[str] = mapped_column(
        db.String(50), nullable=False
    )  # Ejemplo: "entrada", "salida"
    cantidad: Mapped[float] = mapped_column(db.Float, nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(db.DateTime, default=db.func.now())
    motivo: Mapped[str] = mapped_column(db.String(255), nullable=True)
    usuario_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    detalle_compra_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("detalle_compra.id"), nullable=True
    )

    materia_prima = db.relationship("MateriaPrima", back_populates="movimientos")
    usuario = db.relationship("Usuario", back_populates="movimientos_materia_prima")
    detalle_compra = db.relationship(
        "DetalleCompra", back_populates="movimientos_materia_prima"
    )

    # TODO: Agregar relacion con salidas, tanto con mermas con produccion
