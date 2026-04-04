from flask import Blueprint
from .model import MateriaPrima

bp = Blueprint("materias_primas", __name__, url_prefix="/materias_primas", template_folder="templates")
from . import routes
