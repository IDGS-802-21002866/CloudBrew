from flask import Blueprint

from app.modules.presentaciones.model import Presentacion


__all__ = ["Presentacion"]
bp = Blueprint(
    "presentaciones",
    __name__,
    url_prefix="/presentaciones",
    template_folder="templates",
)
from . import routes
