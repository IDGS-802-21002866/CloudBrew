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
    solicitud_compra_id: Mapped[int] = mapped_column(
        db.ForeignKey("solicitud_compra.id"), nullable=True
    )
    solicitud_compra = db.relationship("SolicitudCompra")
    actualizado_por: Mapped[str] = mapped_column(db.String(100), nullable=True)
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

    movimientos_materia_prima = db.relationship(
        "MovimientosMateriaPrima", back_populates="detalle_compra"
    )


class SolicitudCompra(db.Model):
    __tablename__ = "solicitud_compra"
    id = db.Column(db.Integer, primary_key=True)
    materia_prima_id = db.Column(
        db.Integer, db.ForeignKey("materias_primas.id"), nullable=False
    )
    cantidad = db.Column(db.Float, nullable=False)
    origen = db.Column(db.String(20), nullable=False, default="almacen")
    referencia_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=True)
    estado = db.Column(db.String(20), nullable=False, default="Pendiente")
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())

    materia_prima = db.relationship("MateriaPrima")
    referencia = db.relationship("Pedido", foreign_keys=[referencia_id])
