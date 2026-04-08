from flask import flash, redirect, render_template, url_for

from . import bp
from app.modules.inventario_materias_primas.service import (
    InventarioMateriasPrimasService,
)

servicio = InventarioMateriasPrimasService()


@bp.route("/")
def listar():
    inventario = servicio.listar_materias_primas_con_stock()
    return render_template(
        "inventario_materias_primas/listar.html", inventario=inventario
    )


@bp.route("/<int:id>")
def detalle(id):
    try:
        materia_prima = servicio.obtener_materia_prima(id)
        movimientos = servicio.listar_movimientos_materia_prima(id)
        stock_actual = servicio.obtener_stock_actual_materia_prima(id)
        return render_template(
            "inventario_materias_primas/detalle.html",
            materia_prima=materia_prima,
            movimientos=movimientos,
            stock_actual=stock_actual,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("inventario_materias_primas.listar"))
