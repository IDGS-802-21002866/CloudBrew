from flask import Blueprint

from app.modules.ventas.model import Venta, DetalleVenta

bp = Blueprint("ventas", __name__, url_prefix="/ventas", template_folder="templates")

__all__ = ["Venta", "DetalleVenta"]

from . import routes
