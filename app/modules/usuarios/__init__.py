from flask import Blueprint

from app.modules.usuarios.model import Usuario

__all__ = ["Usuario"]
bp = Blueprint("usuarios", __name__, url_prefix="", template_folder="templates")

from . import routes