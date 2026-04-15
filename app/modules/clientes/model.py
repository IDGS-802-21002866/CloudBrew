from sqlalchemy import String, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from datetime import datetime


class Cliente(db.Model):
    __tablename__ = "clientes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Atomización del Nombre
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)

    # Atomización de la Dirección (Obligatoria)
    calle_numero: Mapped[str] = mapped_column(String(150), nullable=False)
    colonia: Mapped[str] = mapped_column(String(100), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo_postal: Mapped[str] = mapped_column(String(10), nullable=False)

    tipo: Mapped[str] = mapped_column(String(20), default="retail")
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    usuario_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("usuario.id"), nullable=True)

    usuario = relationship("Usuario")

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    # Relaciones
    ventas = relationship("Venta", back_populates="cliente")

    @property
    def direccion_completa(self):
        return f"{self.calle_numero}, Col. {self.colonia}, {self.ciudad}, {self.estado}. CP: {self.codigo_postal}"
