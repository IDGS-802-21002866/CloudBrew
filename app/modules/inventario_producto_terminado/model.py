import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app import db


class MovimientosReceta(db.Model):
    __tablename__ = "movimientos_receta"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    receta_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("recetas.id"), nullable=False
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

    receta = db.relationship("Recetas", backref="movimientos")
    usuario = db.relationship("Usuario", back_populates="movimientos_receta")

    # TODO: Agregar relacion con salidas y entradas, tanto con mermas, con produccion y con ventas
