from flask import Blueprint

from app.modules.proc_prod.model import ProcesoProductivo

__all__ = ["ProcesoProductivo"]
bp = Blueprint(
    "proc_prod",
    __name__,
    url_prefix="/procesos_productivos",
    template_folder="templates",
)

from . import routes
