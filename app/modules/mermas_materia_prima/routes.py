from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from . import bp
from .forms import MermaForm
from .service import MermaMateriaPrimaService
from app.modules.inventario_materias_primas import repository as inv_repo
from app.modules.inventario_materias_primas.service import InventarioMateriasPrimasService
from app.modules.unidades_medida.service import UnidadMedidaService
from app.shared.decorators import verificar_rol_o_denegar


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin", "almacen")


medida_service = UnidadMedidaService()
servicio = MermaMateriaPrimaService()
inventario_service = InventarioMateriasPrimasService()


@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")
    pagination = servicio.listar_paginados(
        page=page, per_page=10, search_term=search_term
    )
    return render_template(
        "mermas_materia_prima/listar.html",
        pagination=pagination,
        search_term=search_term,
    )


@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = MermaForm()
    materias_paginadas = inventario_service.listar_materias_primas_paginadas(page=1, per_page=1000)
    materias = materias_paginadas.items

    mp_tipos = {}
    mp_data = {}
    choices = []
    for mp in materias:
        stock_actual = inventario_service.obtener_stock_actual_materia_prima(mp['id'])
        unidad = mp.get('abr', 'G')
        choices.append((mp['id'], f"{mp['nombre']} - Stock: {stock_actual:.2f} {unidad}"))
        mp_tipos[str(mp['id'])] = unidad.upper()
        mp_data[str(mp['id'])] = {
            "stock": float(stock_actual),
            "unidad": unidad.upper(),
        }

    form.materia_prima_id.choices = choices

    if form.validate_on_submit():
        try:
            datos = {
                "materia_prima_id": form.materia_prima_id.data,
                "cantidad": form.cantidad.data,
                "motivo": form.motivo.data,
            }
            servicio.registrar_merma(datos, current_user.id)
            flash("Merma registrada exitosamente.", "success")
            return redirect(url_for("mermas_materia_prima.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "mermas_materia_prima/crear.html",
        form=form,
        mp_tipos=mp_tipos,
        mp_data=mp_data,
    )


@bp.route("/<int:id>")
def detalle(id):
    try:
        merma = servicio.obtener_merma_por_id(id)
        return render_template("mermas_materia_prima/detalle.html", merma=merma)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("mermas_materia_prima.listar"))


@bp.route("/<int:id>/cancelar", methods=["POST"])
def cancelar(id):
    try:
        servicio.cancelar(id)
        flash("Merma cancelada correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("mermas_materia_prima.listar"))
