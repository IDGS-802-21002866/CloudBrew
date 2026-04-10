from app import db

class VentasPorMes(db.Model):
    __tablename__ = 'vw_ventas_por_mes'
    __table_args__ = {'extend_existing': True}

    anio = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.Integer, primary_key=True)
    total_unidades_vendidas = db.Column(db.Float)
    total_pedidos = db.Column(db.Integer)

class MermasPorMes(db.Model):
    __tablename__ = 'vw_mermas_por_mes'
    __table_args__ = {'extend_existing': True}

    anio = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.Integer, primary_key=True)
    total_mermas_unidades = db.Column(db.Float) # Cantidad física
    costo_total_mermas = db.Column(db.Float)    # Sumatoria de precios


class ProductoMasVendido(db.Model):
    __tablename__ = 'vw_top_producto_vendido'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    total_vendido = db.Column(db.Float)


class ProductoMasProducido(db.Model):
    __tablename__ = 'vw_top_producto_producido'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    total_producido = db.Column(db.Float)