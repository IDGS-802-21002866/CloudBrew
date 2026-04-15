from flask import flash, redirect, render_template, request, url_for

from . import bp
from app.shared.decorators import login_required
from app.modules.inventario_producto_terminado.service import (
    InventarioProductoTerminadoService,
)

servicio = InventarioProductoTerminadoService()


@login_required
@bp.route("/")
def listar():
    page=request.args.get("page", 1, type=int)
    inventario = servicio.listar_recetas_con_stock_pag(page, per_page=10)
    return render_template(
        "inventario_producto_terminado/listar.html", pagination=inventario
    )


@login_required
@bp.route("/<int:id>")
def detalle(id):
    try:
        receta = servicio.obtener_receta(id)
        movimientos = servicio.listar_movimientos_receta(id)
        stock_actual = servicio.obtener_stock_actual_receta(id)
        return render_template(
            "inventario_producto_terminado/detalle.html",
            receta=receta,
            movimientos=movimientos,
            stock_actual=stock_actual,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("inventario_producto_terminado.listar"))
