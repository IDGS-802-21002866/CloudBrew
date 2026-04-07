from sqlalchemy import String, Integer, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class UnidadMedida(db.Model):
    __tablename__ = "unidad_medida"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    abreviatura: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    tipo_medida_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tipo_medida.id"), nullable=False
    )
    valor_conversion: Mapped[float] = mapped_column(Numeric(10, 4), default=1.0)
    es_base_sistema: Mapped[bool] = mapped_column(Boolean, default=False)

    tipo_medida: Mapped["TipoMedida"] = relationship(
        "TipoMedida", back_populates="unidades_medida"
    )


class TipoMedida(db.Model):
    __tablename__ = "tipo_medida"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    unidad_base: Mapped[str] = mapped_column(String(50), nullable=False)

    unidades_medida: Mapped[list["UnidadMedida"]] = relationship(
        "UnidadMedida", back_populates="tipo_medida"
    )
