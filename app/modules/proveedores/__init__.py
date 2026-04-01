from flask import Blueprint

bp = Blueprint("proveedores", __name__, url_prefix="", template_folder="templates")

from . import routes
