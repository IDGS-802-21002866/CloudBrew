from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user

from app.modules.usuarios import form

from . import bp
from .forms import MermaProductoTerminadoForm
from .service import MermaProductoTerminadoService
from app.modules.inventario_producto_terminado.service import InventarioProductoTerminadoService
from app.modules.lotes.service import LoteProduccionService

servicio = MermaProductoTerminadoService()
inventario_servicio = InventarioProductoTerminadoService()
lote_servicio = LoteProduccionService()


@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")
    pagination = servicio.listar_paginados(page=page, per_page=10, search_term=search_term)
    return render_template(
        "mermas_producto_terminado/listar.html",
        pagination=pagination,
        search_term=search_term,
    )


# app/modules/mermas_producto_terminado/routes.py

@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = MermaProductoTerminadoForm()
    recetas = inventario_servicio.listar_recetas_con_stock()
    lotes_raw = lote_servicio.obtener_lotes_paginados(per_page=2000).items
    
    lotes_por_receta = {}
    for l in lotes_raw:
        # Usamos getattr para que si 'activo' no existe, asuma True y no truene
        es_activo = getattr(l, 'activo', True) 
        
        if es_activo: 
            try:
                # Accedemos al ID de la receta a través de la producción
                r_id = str(l.produccion.id_receta) 
                if r_id not in lotes_por_receta: 
                    lotes_por_receta[r_id] = []
                
                lotes_por_receta[r_id].append({
                    "id": l.id_lote, 
                    "codigo": l.codigo_lote, 
                    "cantidad": float(l.cantidad_generada)
                })
            except Exception as e:
                # Si un lote no tiene producción ligada, lo ignoramos
                continue

    if request.method == "POST":
        # Recolectamos datos del formulario manual para evitar líos de validación
        datos = {
            "receta_id": request.form.get("receta_id"),
            "cantidad": request.form.get("cantidad"),
            "motivo": request.form.get("motivo"),
            "lote_id": request.form.get("lote_id") or None,
            "es_lote_completo": 'es_lote_completo' in request.form
        }
        try:
            servicio.registrar_merma(datos, current_user.id)
            flash("Merma registrada y stock actualizado correctamente.", "success")
            return redirect(url_for("mermas_producto_terminado.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("mermas_producto_terminado/crear.html", 
                           form=form, 
                           recetas=recetas, 
                           lotes_data=lotes_por_receta)

@bp.route("/stock/<int:receta_id>")
def obtener_stock(receta_id):
    stock_actual = servicio.obtener_stock_actual(receta_id)
    return jsonify({"stock_actual": float(stock_actual)})


@bp.route("/lotes/<int:receta_id>")
def obtener_lotes_por_receta(receta_id):
    lotes = lote_servicio.obtener_por_receta(receta_id)
    resultado = [
        {
            "id_lote": lote.id_lote,
            "codigo_lote": lote.codigo_lote,
            "cantidad_generada": lote.cantidad_generada,
        }
        for lote in lotes
    ]
    return jsonify({"lotes": resultado})


@bp.route("/<int:id>")
def detalle(id):
    try:
        merma = servicio.obtener_merma_por_id(id)
        return render_template("mermas_producto_terminado/detalle.html", merma=merma)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("mermas_producto_terminado.listar"))


@bp.route("/<int:id>/cancelar", methods=["POST"])
def cancelar(id):
    if current_user.rol_id != 1:
        flash("No tienes permiso para cancelar esta merma.", "danger")
        return redirect(url_for("mermas_producto_terminado.detalle", id=id))

    try:
        servicio.cancelar(id)
        flash("Merma cancelada correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("mermas_producto_terminado.listar"))
