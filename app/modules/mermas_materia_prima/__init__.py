from flask import Blueprint
from .model import MermaMateriaPrima

bp = Blueprint(
    "mermas_materia_prima",
    __name__,
    url_prefix="/mermas_materia_prima",
    template_folder="templates",
)

from . import routes

__all__ = ["MermaMateriaPrima"]
