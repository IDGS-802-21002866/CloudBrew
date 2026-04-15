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
    
# Esta ruta es "todoterreno": funciona para /solicitar y para /solicitar/5
@bp.route("/solicitar", defaults={'id': None}, methods=["GET", "POST"])
@bp.route("/solicitar/<int:id>", methods=["GET", "POST"])
def solicitar(id):
    materia = None
    materias = []
    
    if id:
        # Caso: venimos de una fila específica (botón de la tabla)
        materia = servicio.obtener_materia_prima(id)
    else:
        # Caso: venimos del botón verde de arriba (general)
        # Cargamos todas para que el usuario elija en el select
        materias = servicio.listar_materias_primas_paginadas(per_page=100).items

    if request.method == "POST":
        materia_id = id or request.form.get("materia_prima_id")
        cantidad = request.form.get("cantidad")
        motivo = request.form.get("motivo")
        
        # Aquí es donde se conectaría con la lógica de SolicitudCompra
        # Por ahora el flash para confirmar que funciona
        nombre_materia = materia.nombre if materia else "Materia"
        flash(f"Solicitud de {cantidad} para {nombre_materia} enviada a Compras", "success")
        return redirect(url_for("inventario_materias_primas.listar"))
        
    return render_template("inventario_materias_primas/solicitar.html", materia=materia, materias=materias)
