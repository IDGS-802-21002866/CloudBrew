from app import db


class PedidoProduccion(db.Model):
    __tablename__ = "pedido_produccion"

    id_pedido_produccion = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    id_produccion = db.Column(
        db.Integer, db.ForeignKey("produccion.id_produccion"), nullable=False
    )

    pedido = db.relationship("Pedido", back_populates="producciones")
    produccion = db.relationship("Produccion", back_populates="pedidos")

    def __repr__(self):
        return f"<PedidoProduccion {self.id_pedido_produccion}>"
