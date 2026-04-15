from flask import flash, redirect, render_template, request, url_for

from . import bp
from app.modules.inventario_materias_primas.service import (
    InventarioMateriasPrimasService,
)

servicio = InventarioMateriasPrimasService()


@bp.route("/")
def listar():
    page = request.args.get('page', 1, type=int)
    search_term = request.args.get('q', '')
    
    pagination = servicio.listar_materias_primas_paginadas(page=page, per_page=10, search_term=search_term)
    
    return render_template(
        "inventario_materias_primas/listar.html", 
        pagination=pagination,
        search_term=search_term
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
