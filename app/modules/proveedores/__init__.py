from flask import Blueprint
from .model import Proveedor

bp = Blueprint(
    "proveedores", __name__, url_prefix="/proveedores", template_folder="templates"
)
__all__ = ["Proveedor"]
from . import routes
