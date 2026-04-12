from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Recetas(db.Model):
    __tablename__ = "recetas"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(db.String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(db.Text, nullable=True)
    cantidad_producida: Mapped[float] = mapped_column(db.Float, nullable=False)
    activo: Mapped[bool] = mapped_column(db.Boolean, default=True)
    precio_venta: Mapped[float] = mapped_column(db.Float, nullable=True)
    imagen: Mapped[bytes] = mapped_column(db.LargeBinary, nullable=True)
    imagen_tipo: Mapped[str] = mapped_column(db.String(50), nullable=True)
    usuario_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)

    usuario = db.relationship("Usuario")
    produccion = db.relationship("Produccion", back_populates="receta")
    detalle = db.relationship("RecetaDetalle", back_populates="receta")
    procesos_receta = db.relationship("ProcesosReceta", back_populates="receta")
    producciones = db.relationship("Produccion", back_populates="receta")


class RecetaDetalle(db.Model):
    __tablename__ = "receta_detalle"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    receta_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("recetas.id"), nullable=False
    )
    materia_prima_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("materias_primas.id"), nullable=False
    )
    cantidad: Mapped[float] = mapped_column(db.Float, nullable=False)

    receta = db.relationship("Recetas", back_populates="detalle")
    materia_prima = db.relationship("MateriaPrima", back_populates="recetas_detalle")


class ProcesosReceta(db.Model):
    __tablename__ = "procesos_receta"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    receta_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("recetas.id"), nullable=False
    )
    proceso_productivo_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("procesos_productivos.id"), nullable=False
    )
    receta = db.relationship("Recetas", back_populates="procesos_receta")
    proceso_productivo = db.relationship(
        "ProcesoProductivo", back_populates="procesos_receta"
    )
    tiempo_estimado: Mapped[float] = mapped_column(db.Float, nullable=False)
    orden: Mapped[int] = mapped_column(db.Integer, default=0)
