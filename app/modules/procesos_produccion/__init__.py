from flask import Blueprint

bp = Blueprint(
    "procesos_produccion",
    __name__,
    url_prefix="/procesos_produccion",
    template_folder="templates",
)

from . import routes
