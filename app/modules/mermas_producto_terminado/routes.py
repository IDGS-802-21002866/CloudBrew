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
    form.receta_id.choices = [("", "Seleccione una receta")] + [
        (r.id, r.nombre) for r in recetas
    ]
    lotes_por_receta = {}
    lotes_choices = [(None, "Seleccione un lote")]

    for l in lotes_raw:
        es_activo = getattr(l, "activo", True)

        if es_activo:
            try:
                r_id = str(l.produccion.id_receta)

                if r_id not in lotes_por_receta:
                    lotes_por_receta[r_id] = []

                lote_info = {
                    "id": l.id_lote,
                    "codigo": l.codigo_lote,
                    "cantidad": float(l.cantidad_generada),
                }

                lotes_por_receta[r_id].append(lote_info)

                lotes_choices.append(
                    (l.id_lote, f"{l.codigo_lote} - {l.cantidad_generada:.2f}")
                )

            except Exception:
                continue

    form.lote_id.choices = lotes_choices

    if form.validate_on_submit():
        try:
            datos = {
                "receta_id": form.receta_id.data,
                "cantidad": form.cantidad.data,
                "motivo": form.motivo.data,
                "lote_id": form.lote_id.data,
                "es_lote_completo": form.es_lote_completo.data,
            }

            servicio.registrar_merma(datos, current_user.id)

            flash("Merma registrada y stock actualizado correctamente.", "success")
            return redirect(url_for("mermas_producto_terminado.listar"))

        except ValueError as e:
            flash(str(e), "danger")

    if form.errors:
        for field, errores in form.errors.items():
            for error in errores:
                flash(f"{field}: {error}", "danger")

    return render_template(
        "mermas_producto_terminado/crear.html",
        form=form,
        recetas=recetas,
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
