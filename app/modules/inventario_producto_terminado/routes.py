from flask import flash, redirect, render_template, url_for

from . import bp
from app.modules.inventario_producto_terminado.service import (
    InventarioProductoTerminadoService,
)

servicio = InventarioProductoTerminadoService()


@bp.route("/")
def listar():
    inventario = servicio.listar_recetas_con_stock()
    return render_template(
        "inventario_producto_terminado/listar.html", inventario=inventario
    )


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
