from flask import Blueprint

bp = Blueprint("costos", __name__, url_prefix="/costos", template_folder="templates")

from app.modules.costos import routes  # noqa: E402, F401
