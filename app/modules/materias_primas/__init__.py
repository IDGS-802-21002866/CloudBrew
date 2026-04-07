from flask import Blueprint
from .model import MateriaPrima

__all__ = ["MateriaPrima"]
bp = Blueprint(
    "materias_primas",
    __name__,
    url_prefix="/materias_primas",
    template_folder="templates",
)
from . import routes
