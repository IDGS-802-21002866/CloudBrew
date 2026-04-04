from flask import Blueprint

from app.modules.usuarios.model import Usuario, Rol

__all__ = ["Usuario", "Rol"]
bp = Blueprint("usuarios", __name__, url_prefix="", template_folder="templates")

from . import routes
