from flask import Blueprint

from app.modules.produccion.model import Produccion, ProduccionProceso

__all__ = ["Produccion", "ProduccionProceso"]
bp = Blueprint("produccion", __name__, url_prefix="", template_folder="templates")

from . import routes
