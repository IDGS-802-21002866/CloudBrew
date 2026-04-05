from flask import Blueprint

bp = Blueprint("clientes", __name__, url_prefix="/clientes", template_folder="templates")
from . import routes