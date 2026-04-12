from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.modules.main import bp
from app.modules.dashboard.services import DashboardService
from app.shared.decorators import login_required

dashboard_service = DashboardService()


@login_required
@bp.route("/", methods=["GET"])
def index():
    return render_template("main/index.html")


@login_required
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
