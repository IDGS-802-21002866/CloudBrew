from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from . import bp
from .forms import MermaForm
from .service import MermaMateriaPrimaService
from app.modules.inventario_materias_primas import repository as inv_repo
from app.shared.decorators import login_required
from app.modules.unidades_medida.service import UnidadMedidaService

medida_service = UnidadMedidaService()
servicio = MermaMateriaPrimaService()


@login_required
@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")
    pagination = servicio.listar_paginados(page=page, per_page=10, search_term=search_term)
    return render_template(
        "mermas_materia_prima/listar.html",
        pagination=pagination,
        search_term=search_term,
    )


@login_required
@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = MermaForm()
    materias = inv_repo.get_all_materias_primas_con_stock()
    form.materia_prima_id.choices = [
        (mp.id, f"{mp.nombre} - Stock: {mp.stock_actual:.2f}") for mp in materias
    ]
    medidas=medida_service.listar_unidades_medida()
    form.medida.choices = [(m.id, m.nombre) for m in medidas]
    medida_tipos = {str(m.id): str(m.tipo_medida_id) for m in medidas}
    mp_tipos = {str(mp.id): str(mp.tipo_medida_id) for mp in materias}

    if form.validate_on_submit():
        try:
            medida=medida_service.obtener_unidad_medida(form.medida.data)
            cantidad_en_unidad_base = form.cantidad.data * medida.valor_conversion
            datos = {
                "materia_prima_id": form.materia_prima_id.data,
                "cantidad": cantidad_en_unidad_base,
                "motivo": form.motivo.data,
            }
            servicio.registrar_merma(datos, current_user.id)
            flash("Merma registrada exitosamente.", "success")
            return redirect(url_for("mermas_materia_prima.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("mermas_materia_prima/crear.html", form=form, medidas=medidas, 
                           medida_tipos=medida_tipos,mp_tipos=mp_tipos)


@login_required
@bp.route("/<int:id>")
def detalle(id):
    try:
        merma = servicio.obtener_merma_por_id(id)
        return render_template("mermas_materia_prima/detalle.html", merma=merma)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("mermas_materia_prima.listar"))


@login_required
@bp.route("/<int:id>/cancelar", methods=["POST"])
def cancelar(id):
    try:
        servicio.cancelar(id)
        flash("Merma cancelada correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("mermas_materia_prima.listar"))
