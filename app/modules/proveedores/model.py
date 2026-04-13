from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Proveedor(db.Model):
    __tablename__ = "proveedor"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    direccion: Mapped[str] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    usuario_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("usuario.id"), nullable=True)

    usuario = relationship("Usuario")
    compras = db.relationship(
        "Compra", back_populates="proveedor", cascade="all, delete-orphan"
    )
