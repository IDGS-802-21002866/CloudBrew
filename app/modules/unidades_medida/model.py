from sqlalchemy import String, Integer, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

class UnidadMedida(db.Model):
    __tablename__ = "unidad_medida"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    abreviatura: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    es_base: Mapped[bool] = mapped_column(Boolean, default=False)
    

    unidad_base_id: Mapped[int] = mapped_column(Integer, ForeignKey('unidad_medida.id'), nullable=True)
    valor_conversion: Mapped[float] = mapped_column(Numeric(10,4), nullable=True)


    unidad_base = relationship('UnidadMedida', remote_side=[id], backref='unidades_derivadas')