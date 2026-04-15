from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user

from app.modules.usuarios import form

from . import bp
from .forms import MermaProductoTerminadoForm
from .service import MermaProductoTerminadoService
from app.modules.inventario_producto_terminado.service import (
    InventarioProductoTerminadoService,
)
from app.modules.lotes.service import LoteProduccionService
from app.shared.decorators import verificar_rol_o_denegar


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin", "almacen")


servicio = MermaProductoTerminadoService()
inventario_servicio = InventarioProductoTerminadoService()
lote_servicio = LoteProduccionService()


@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")
    pagination = servicio.listar_paginados(
        page=page, per_page=10, search_term=search_term
    )
    return render_template(
        "mermas_producto_terminado/listar.html",
        pagination=pagination,
        search_term=search_term,
    )


# app/modules/mermas_producto_terminado/routes.py

@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = MermaProductoTerminadoForm()
    
    # 1. Obtener datos
    recetas = inventario_servicio.listar_recetas_con_stock()
    lotes_raw = lote_servicio.obtener_lotes_paginados(per_page=5000).items

    # 2. Configurar opciones del selector de Recetas (ACCESO POR DICCIONARIO)
    form.receta_id.choices = [("", "-- Seleccionar Cerveza --")] + [
        (str(r['id']), f"{r['nombre']} (Total: {r['stock_actual']})") for r in recetas
    ]

    # 3. Preparar el JSON para el JS y configurar choices de Lotes
    lotes_por_receta = {}
    todos_los_lotes_choices = [("", "-- Selecciona el lote --")]

    for l in lotes_raw:
        try:
            # Intentar acceso como objeto, si falla, intentar como diccionario
            if hasattr(l, 'produccion'):
                r_id = str(l.produccion.id_receta)
                l_id = l.id_lote
                l_codigo = l.codigo_lote
                l_cantidad = float(l.cantidad_generada)
            else:
                # Si lotes_raw también son diccionarios
                r_id = str(l['produccion']['id_receta'])
                l_id = l['id_lote']
                l_codigo = l['codigo_lote']
                l_cantidad = float(l['cantidad_generada'])
            
            # Estructura para JavaScript
            if r_id not in lotes_por_receta:
                lotes_por_receta[r_id] = []
            
            lotes_por_receta[r_id].append({
                "id": l_id,
                "codigo": l_codigo,
                "cantidad": l_cantidad,
            })
            
            # Choices para validación de WTForms
            todos_los_lotes_choices.append((str(l_id), f"{l_codigo}"))
            
        except (AttributeError, KeyError, TypeError):
            continue

    form.lote_id.choices = todos_los_lotes_choices

    # 4. Procesar el Formulario
    if form.validate_on_submit():
        datos = {
            "receta_id": form.receta_id.data,
            "cantidad": form.cantidad.data,
            "motivo": form.motivo.data,
            "lote_id": form.lote_id.data if form.lote_id.data else None,
            "es_lote_completo": form.es_lote_completo.data
        }
        
        try:
            servicio.registrar_merma(datos, current_user.id)
            flash("Merma registrada correctamente.", "success")
            return redirect(url_for("mermas_producto_terminado.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "mermas_producto_terminado/crear.html",
        form=form,
        lotes_data=lotes_por_receta,
    )
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
