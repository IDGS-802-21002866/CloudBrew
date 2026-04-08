from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Compra(db.Model):
    __tablename__ = "compra"
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha_registro: Mapped[str] = mapped_column(
        db.DateTime, nullable=False, default=db.func.now()
    )
    fecha_compra: Mapped[str] = mapped_column(db.DateTime, nullable=True)
    cancelada: Mapped[bool] = mapped_column(db.Boolean, default=False)
    proveedor_id: Mapped[int] = mapped_column(db.ForeignKey("proveedor.id"))
    proveedor = db.relationship("Proveedor", back_populates="compras")
    usuario_id: Mapped[int] = mapped_column(db.ForeignKey("usuario.id"))
    usuario = db.relationship("Usuario")
    detalles = db.relationship(
        "DetalleCompra", back_populates="compra", cascade="all, delete-orphan"
    )


class DetalleCompra(db.Model):
    __tablename__ = "detalle_compra"
    id: Mapped[int] = mapped_column(primary_key=True)
    compra_id: Mapped[int] = mapped_column(db.ForeignKey("compra.id"))
    compra = db.relationship("Compra", back_populates="detalles")
    materia_prima_id: Mapped[int] = mapped_column(db.ForeignKey("materias_primas.id"))
    materia_prima = db.relationship("MateriaPrima", back_populates="compras")
    presentacion_id: Mapped[int] = mapped_column(db.ForeignKey("presentaciones.id"))
    presentacion = db.relationship("Presentacion")
    cantidad: Mapped[int] = mapped_column(db.Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(db.Float, nullable=False)
