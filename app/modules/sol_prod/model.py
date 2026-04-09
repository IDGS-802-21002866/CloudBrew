from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import app

db = app.db

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id_pedido = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    fecha_pedido = db.Column(db.Date, default=datetime.now, nullable=False)
    estado = db.Column(db.String(50), nullable=False)

    # Relación
    detalles = db.relationship('DetallePedido', back_populates='pedido', cascade='all, delete-orphan')
    detalles = db.relationship('clientes', back_populates='pedido', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Pedido {self.id_pedido}>"


class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'

    id_detalle_pedido = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_receta = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)

    pedido = db.relationship('Pedido', back_populates='detalles')
    receta = db.relationship('Recetas', back_populates='detalles')

    def __repr__(self):
        return f"<DetallePedido {self.id_detalle_pedido}>"

class PedidoProduccion(db.Model):
    __tablename__ = 'pedido_produccion'

    id_pedido_produccion = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_produccion = db.Column(db.Integer, db.ForeignKey('produccion.id_produccion'), nullable=False)

    pedido = db.relationship('Pedido', back_populates='producciones')
    produccion = db.relationship('Produccion', back_populates='pedidos')

    def __repr__(self):
        return f"<PedidoProduccion {self.id_pedido_produccion}>"