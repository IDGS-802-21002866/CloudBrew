from flask import render_template

from app.modules.costos import bp
from app.modules.costos.service import CostoService
from app.shared.decorators import verificar_rol_o_denegar


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin", "ventas")


costo_service = CostoService()


@bp.route("/")
def dashboard():
    data = costo_service.listar_dashboard()
    return render_template("costos/dashboard.html", **data)
