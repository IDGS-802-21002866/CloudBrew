from app import db

class Produccion(db.Model):
    __tablename__ = 'produccion'

    id_produccion = db.Column(db.Integer, primary_key=True)
    id_receta = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(50))
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    receta = db.relationship(
        'Recetas',
        back_populates='produccion'
    )

    procesos = db.relationship(
        'ProduccionProceso',
        back_populates='produccion',
        cascade='all, delete-orphan'
    )

    lotes = db.relationship(
        'LoteProduccion',
        back_populates='produccion',
        cascade='all, delete-orphan'
    )

    pedidos = db.relationship(
        'PedidoProduccion',
        back_populates='produccion',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Produccion {self.id_produccion}>"

class ProduccionProceso(db.Model):
    __tablename__ = 'produccion_proceso'

    id_produccion_proceso = db.Column(db.Integer, primary_key=True)
    id_produccion = db.Column(db.Integer, db.ForeignKey('produccion.id_produccion'), nullable=False)
    id_proceso = db.Column(db.Integer, db.ForeignKey('procesos_productivos.id'), nullable=False)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(50))

    produccion = db.relationship('Produccion', back_populates='procesos')
    proceso = db.relationship('ProcesoProductivo', back_populates='producciones')

    def __repr__(self):
        return f"<ProduccionProceso {self.id_produccion_proceso}>"