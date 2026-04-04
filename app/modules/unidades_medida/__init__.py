from flask import Blueprint
from .model import UnidadMedida
bp = Blueprint("unidades_medida", __name__, url_prefix="/unidades_medida", template_folder="templates")
from . import routes
