from flask import Blueprint

bp = Blueprint("presentaciones", __name__, url_prefix="/presentaciones", template_folder="templates")
from . import routes
