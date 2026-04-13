
from flask import Blueprint


bp = Blueprint("backup", __name__, url_prefix="/backup", template_folder="templates/respaldo")

from app.modules.respaldo import routes