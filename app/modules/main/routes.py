from flask import render_template, redirect, url_for
from flask_login import current_user
from app.modules.main import bp
from app.modules.dashboard.services import DashboardService
from app.shared.decorators import verificar_rol_o_denegar


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin", "almacen", "compras", "ventas")


dashboard_service = DashboardService()


@bp.route("/", methods=["GET"])
def index():
    if current_user.rol and current_user.rol.name == "admin":
        return redirect(url_for("main.dashboard"))
    return render_template("main/index.html")


@bp.route("/dashboard", methods=["GET"])
def dashboard():
    if not current_user.rol or current_user.rol.name != "admin":
        return redirect(url_for("main.index"))
    mas_vendido = dashboard_service.get_producto_mas_vendido()
    mas_producido = dashboard_service.get_producto_mas_producido()
    ventas = dashboard_service.get_ventas_por_mes()
    mermas = dashboard_service.get_mermas_por_mes()
    utilidad_productos = dashboard_service.get_utilidad_productos(limit=5)

    return render_template(
        "main/dashboard.html",
        mas_vendido=mas_vendido,
        mas_producido=mas_producido,
        ventas=ventas,
        mermas=mermas,
        utilidad_productos=utilidad_productos,
    )
