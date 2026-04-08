from flask import Blueprint

from app.modules.inventario_producto_terminado.model import MovimientosReceta

bp = Blueprint(
    "inventario_producto_terminado",
    __name__,
    url_prefix="/inventario_producto_terminado",
    template_folder="templates",
)

from . import routes

__all__ = ["MovimientosReceta"]
