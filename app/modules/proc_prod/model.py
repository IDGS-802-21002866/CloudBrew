from sqlalchemy import String
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class ProcesoProductivo(db.Model, UserMixin):
    __tablename__ = "procesos_productivos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str] = mapped_column(String(200), nullable=True)
    activo: Mapped[bool] = mapped_column(default=True)

    procesos_receta = db.relationship(
        "ProcesosReceta", back_populates="proceso_productivo"
    )
