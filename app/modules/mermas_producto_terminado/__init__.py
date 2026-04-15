from flask import Blueprint
from .model import MermaProductoTerminado

bp = Blueprint(
    "mermas_producto_terminado",
    __name__,
    url_prefix="/mermas-producto-terminado",
    template_folder="templates",
)

from . import routes

__all__ = ["MermaProductoTerminado"]
