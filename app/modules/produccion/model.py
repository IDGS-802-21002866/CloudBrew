from sqlalchemy import String
from app import db


class Produccion(db.Model):
    __tablename__ = "produccion"

    id_produccion = db.Column(db.Integer, primary_key=True)
    id_receta = db.Column(db.Integer, db.ForeignKey("recetas.id"), nullable=False)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(50))
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)

    usuario = db.relationship("Usuario")
    es_retail = db.Column(db.Boolean, default=False, nullable=False)
    id_solicitud_compra = db.Column(
        db.Integer, db.ForeignKey("solicitud_compra.id"), nullable=True
    )
    solicitud_compra = db.relationship("SolicitudCompra", foreign_keys=[id_solicitud_compra])
    receta = db.relationship("Recetas", back_populates="producciones")

    procesos = db.relationship(
        "ProduccionProceso", back_populates="produccion", cascade="all, delete-orphan"
    )

    lotes = db.relationship(
        "LoteProduccion", back_populates="produccion", cascade="all, delete-orphan"
    )

    pedidos = db.relationship(
        "PedidoProduccion", back_populates="produccion", cascade="all, delete-orphan"
    )

    movimientos_materia_prima = db.relationship(
        "MovimientosMateriaPrima", back_populates="produccion"
    )

    def __repr__(self):
        return f"<Produccion {self.id_produccion}>"


class ProduccionProceso(db.Model):
    __tablename__ = "produccion_proceso"

    id_produccion_proceso = db.Column(db.Integer, primary_key=True)
    id_produccion = db.Column(
        db.Integer, db.ForeignKey("produccion.id_produccion"), nullable=False
    )
    id_proceso = db.Column(
        db.Integer, db.ForeignKey("procesos_productivos.id"), nullable=False
    )
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(50))
    orden = db.Column(db.Integer, default=0)
    tiempo_estimado = db.Column(db.Float, nullable=True)

    produccion = db.relationship("Produccion", back_populates="procesos")
    proceso = db.relationship("ProcesoProductivo", back_populates="producciones")

    def __repr__(self):
        return f"<ProduccionProceso {self.id_produccion_proceso}>"
