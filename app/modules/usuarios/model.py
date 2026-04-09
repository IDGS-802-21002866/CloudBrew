import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Rol(db.Model):
    __tablename__ = "rol"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(255))
    usuarios: Mapped["Usuario"] = relationship(back_populates="rol")


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    activo: Mapped[bool] = mapped_column(default=True)
    fs_uniquifier: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4().hex)
    )
    reset_token: Mapped[str] = mapped_column(String(255), nullable=True)
    reset_token_expiry: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("rol.id"))
    rol: Mapped["Rol"] = relationship(back_populates="usuarios")
    movimientos_materia_prima = relationship(
        "MovimientosMateriaPrima", back_populates="usuario"
    )
    movimientos_receta = relationship("MovimientosReceta", back_populates="usuario")

    @property
    def is_active(self):
        """Propiedad requerida por UserMixin de Flask-Login"""
        return self.activo
