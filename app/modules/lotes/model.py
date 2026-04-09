from app import db


class LoteProduccion(db.Model):
    __tablename__ = "lotes_produccion"

    id_lote = db.Column(db.Integer, primary_key=True)
    id_produccion = db.Column(
        db.Integer, db.ForeignKey("produccion.id_produccion"), nullable=False
    )
    codigo_lote = db.Column(db.String(100), nullable=False)
    fecha_produccion = db.Column(db.Date)
    cantidad_generada = db.Column(db.Float)

    produccion = db.relationship("Produccion", back_populates="lotes")
    movimientos_materia_prima = db.relationship(
        "MovimientosMateriaPrima", back_populates="lote_produccion"
    )

    def __repr__(self):
        return f"<LoteProduccion {self.id_lote}>"
