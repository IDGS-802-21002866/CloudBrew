from flask import render_template

from app.modules.costos import bp
from app.modules.costos.service import CostoService

costo_service = CostoService()


@bp.route("/")
def dashboard():
    data = costo_service.listar_dashboard()
    return render_template("costos/dashboard.html", **data)
