from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class ProcesoProductivo(db.Model):
    __tablename__ = "procesos_productivos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str] = mapped_column(String(200), nullable=True)
    activo: Mapped[bool] = mapped_column(default=True)

    procesos_receta = db.relationship(
        "ProcesosReceta", back_populates="proceso_productivo"
    )
    producciones = db.relationship("ProduccionProceso", back_populates="proceso")
