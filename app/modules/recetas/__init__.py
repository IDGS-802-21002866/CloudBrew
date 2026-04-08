from flask import Blueprint

from app.modules.recetas.model import RecetaDetalle, Recetas, ProcesosReceta

__all__ = ["Recetas", "RecetaDetalle", "ProcesosReceta"]

bp = Blueprint("recetas", __name__, url_prefix="/recetas", template_folder="templates")

from app.modules.recetas import routes
