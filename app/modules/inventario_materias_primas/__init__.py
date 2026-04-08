from flask import Blueprint

from app.modules.inventario_materias_primas.model import MovimientosMateriaPrima

bp = Blueprint(
    "inventario_materias_primas",
    __name__,
    url_prefix="/inventario_materias_primas",
    template_folder="templates",
)

from . import routes

__all__ = ["MovimientosMateriaPrima"]
