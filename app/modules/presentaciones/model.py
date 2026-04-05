from sqlalchemy import String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

class Presentacion(db.Model):
    __tablename__ = "presentaciones"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    id_unidad: Mapped[int] = mapped_column(Integer, ForeignKey('unidad_medida.id'), nullable=False)
    cantidad_equivalente: Mapped[float] = mapped_column(Float, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    unidad = relationship("UnidadMedida")