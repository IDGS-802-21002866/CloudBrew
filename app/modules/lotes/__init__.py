from flask import Blueprint

from app.modules.lotes.model import LoteProduccion

__all__ = ["LoteProduccion"]
bp = Blueprint("lotes", __name__, url_prefix="", template_folder="templates")

from . import routes
