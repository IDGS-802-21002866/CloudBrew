from flask import Blueprint
from app.modules.compras.model import Compra, DetalleCompra

bp = Blueprint("compras", __name__, url_prefix="/compras", template_folder="templates")
__all__ = ["Compra", "DetalleCompra"]
