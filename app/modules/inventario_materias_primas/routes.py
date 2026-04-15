from flask import flash, redirect, render_template, request, url_for

from . import bp
from app.modules.compras.service import ComprasService
from app.modules.inventario_materias_primas.service import (
    InventarioMateriasPrimasService,
)

servicio = InventarioMateriasPrimasService()
compras_service = ComprasService()


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
    
# app/modules/inventario_materias_primas/routes.py

@bp.route("/solicitar", defaults={'id': None}, methods=["GET", "POST"])
@bp.route("/solicitar/<int:id>", methods=["GET", "POST"])
def solicitar(id):
    materia = None
    materias = []
    
    if id:
        materia = servicio.obtener_materia_prima(id)
    else:
        # Cargamos materias para el select
        materias = servicio.listar_materias_primas_paginadas(per_page=100).items

    if request.method == "POST":
        materia_id = id or request.form.get("materia_prima_id")
        cantidad = request.form.get("cantidad")
        motivo = request.form.get("motivo")
        
        try:
            # Quitamos el flash de aquí. El servicio se encarga.
            compras_service.crear_solicitud_compra(
                materia_prima_id=materia_id,
                cantidad=float(cantidad),
                origen="almacen",
            )
            return redirect(url_for("inventario_materias_primas.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("inventario_materias_primas/solicitar.html", materia=materia, materias=materias)