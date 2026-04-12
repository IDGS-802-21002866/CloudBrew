from datetime import datetime, date
from sqlalchemy import Date, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy

from app import db


class BitacoraLogin(db.Model):
    __tablename__ = "bitacora_login"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    hora: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    nombre_usuario: Mapped[str] = mapped_column(String(100),nullable=False)
    auth: Mapped[bool] = mapped_column(default=False, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100),nullable=True)
