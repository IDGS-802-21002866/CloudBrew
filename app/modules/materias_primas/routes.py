from flask import render_template, request, redirect, url_for, flash
from app.modules.materias_primas.form import MateriaPrimaForm
from app.modules.materias_primas.service import MateriaPrimaService
from app.modules.unidades_medida.service import UnidadMedidaService
from app.shared.decorators import verificar_rol_o_denegar
from . import bp


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin", "almacen", "compras")


servicio = MateriaPrimaService()
servicio_unidades = UnidadMedidaService()


@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    pagination = servicio.listar_materias_paginadas(page=page, per_page=5)
    return render_template("materias_primas/listar.html", pagination=pagination)


@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = MateriaPrimaForm()
    tipos_medida = servicio_unidades.listar_tipos_medida()
    form.tipo_medida_id.choices = [(t.id, t.nombre) for t in tipos_medida]
    tipo_unidades = {str(t.id): t.unidad_base for t in tipos_medida}

    if form.validate_on_submit():
        try:
            data = {
                "nombre": form.nombre.data,
                "descripcion": form.descripcion.data,
                "tipo_medida_id": form.tipo_medida_id.data,
                "stock_minimo": form.stock_minimo.data,
            }
            servicio.crear_materia(data)
            flash("Materia prima creada exitosamente.", "success")
            return redirect(url_for("materias_primas.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "materias_primas/crear.html", form=form, tipo_unidades=tipo_unidades
    )


@bp.route("/<int:id>")
def detalle(id):
    try:
        materia = servicio.obtener_por_id(id)
        return render_template("materias_primas/detalle.html", materia=materia)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("materias_primas.listar"))


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        materia = servicio.obtener_por_id(id)
        form = MateriaPrimaForm(obj=materia)

        tipos_medida = servicio_unidades.listar_tipos_medida()
        form.tipo_medida_id.choices = [(t.id, t.nombre) for t in tipos_medida]
        tipo_unidades = {str(t.id): t.unidad_base for t in tipos_medida}

        if form.validate_on_submit():
            try:
                data = {
                    "nombre": form.nombre.data,
                    "descripcion": form.descripcion.data,
                    "tipo_medida_id": form.tipo_medida_id.data,
                    "stock_minimo": form.stock_minimo.data,
                }
                servicio.actualizar_materia(id, data)
                flash("Materia prima actualizada exitosamente.", "success")
                return redirect(url_for("materias_primas.detalle", id=id))
            except ValueError as e:
                flash(str(e), "danger")

        return render_template(
            "materias_primas/crear.html",
            form=form,
            materia=materia,
            tipo_unidades=tipo_unidades,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("materias_primas.listar"))


@bp.route("/<int:id>/desactivar", methods=["POST"])
def desactivar(id):
    try:
        servicio.desactivar_materia(id)
        flash("Materia prima desactivada.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("materias_primas.listar"))


@bp.route("/<int:id>/activar", methods=["POST"])
def activar(id):
    try:
        servicio.activar_materia(id)
        flash("Materia prima activada exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("materias_primas.listar"))
