from flask_sqlalchemy import SQLAlchemy
from app import db

class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre       = db.Column(db.String(100), nullable=False)
    telefono     = db.Column(db.String(20),  nullable=True)
    email        = db.Column(db.String(100), nullable=True)
    direccion    = db.Column(db.String(255), nullable=True)
    activo    = db.Column(db.Boolean, nullable=False, default=True)