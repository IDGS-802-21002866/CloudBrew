from flask import Blueprint

from app.modules.bitacora_login.model import BitacoraLogin

__all__ = ["BitacoraLogin"]

bp = Blueprint(
    "bitacora", __name__, url_prefix="/bitacora", template_folder="templates/bitacora"
)

from . import routes