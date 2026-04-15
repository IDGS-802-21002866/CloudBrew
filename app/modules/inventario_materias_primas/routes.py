from flask import flash, redirect, render_template, request, url_for

from . import bp
from app.modules.inventario_materias_primas.service import (
    InventarioMateriasPrimasService,
)
from app.shared.decorators import login_required

servicio = InventarioMateriasPrimasService()


@login_required
@bp.route("/")
def listar():
    page=request.args.get('page', 1, type=int)
    inventario = servicio.listar_materias_primas_con_stock_pag(page=page, per_page=10)
    return render_template(
        "inventario_materias_primas/listar.html", pagination=inventario
    )


@login_required
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
