from flask import render_template
from app.modules.main import bp
from app.modules.dashboard.services import DashboardService

dashboard_service = DashboardService()


@bp.route("/", methods=["GET"])
def index():
    return render_template("main/index.html")


@bp.route("/dashboard", methods=["GET"])
def dashboard():
    mas_vendido = dashboard_service.get_producto_mas_vendido()
    mas_producido = dashboard_service.get_producto_mas_producido()
    ventas = dashboard_service.get_ventas_por_mes()
    mermas = dashboard_service.get_mermas_por_mes()
    
    return render_template(
        "main/dashboard.html",
        mas_vendido=mas_vendido,
        mas_producido=mas_producido,
        ventas=ventas,
        mermas=mermas
    )
