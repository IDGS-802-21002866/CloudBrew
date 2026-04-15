from flask import Blueprint

bp = Blueprint("tienda", __name__, url_prefix="/tienda", template_folder="templates")

from . import routes
