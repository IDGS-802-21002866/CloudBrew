from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class ProductoVenta(db.Model):
    __tablename__ = "producto_venta"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    receta_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("recetas.id"), nullable=False
    )
    presentacion_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("presentaciones.id"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False, default="web")
    cantidad_unidades: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_venta: Mapped[float] = mapped_column(Float, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    usuario_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("usuario.id"), nullable=True
    )

    receta = relationship("Recetas")
    presentacion = relationship("Presentacion")
    usuario = relationship("Usuario")
