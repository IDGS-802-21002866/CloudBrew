from flask import flash, render_template, request, redirect, url_for
from app.modules.proc_prod.form import ProcesoProductivoForm
from app.modules.proc_prod.service import ProcesoProductivoService
from . import bp

servicio = ProcesoProductivoService()


@bp.route("/")
def listar():
    try:
        page = request.args.get("page", 1, type=int)
        querry = request.args.get("querry", "", type=str)
        pag = servicio.listar_procesos(page=page, per_page=5, querry=querry)
        procesos = pag.items
        pagination = {
            "page": pag.page,
            "pages": list(range(1, pag.pages + 1)),
            "has_prev": pag.has_prev,
            "has_next": pag.has_next,
            "prev_num": pag.prev_num,
            "next_num": pag.next_num,
            "total": pag.total,
            "start": (pag.page - 1) * pag.per_page + 1 if pag.total > 0 else 0,
            "end": min(pag.page * pag.per_page, pag.total),
        }
        return render_template(
            "procesos_productivos/listar.html", procesos=procesos, pagination=pagination
        )

    except ValueError as e:
        flash(str(e), "danger")
        return render_template("procesos_productivos/listar.html", procesos=[])


@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = ProcesoProductivoForm()
    if form.validate_on_submit():
        try:
            servicio.crear_proceso(form)
            flash("Proceso productivo creado exitosamente", "success")
            return redirect(url_for("proc_prod.listar"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("procesos_productivos/crear.html", form=form)


@bp.route("/<int:id>")
def detalle(id):
    try:
        proceso = servicio.obtener_por_id(id)
        form = ProcesoProductivoForm(obj=proceso)
        return render_template(
            "procesos_productivos/detalle.html", proceso=proceso, form=form
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("proc_prod.listar"))


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        proceso = servicio.obtener_por_id(id)
        form = ProcesoProductivoForm(obj=proceso)
        if form.validate_on_submit():
            try:
                servicio.actualizar_proceso(id, form)
                flash("Proceso productivo actualizado exitosamente", "success")
                return redirect(url_for("proc_prod.detalle", id=id))
            except ValueError as e:
                flash(str(e), "danger")
        return render_template(
            "procesos_productivos/crear.html", form=form, proceso=proceso
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("proc_prod.listar"))


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        servicio.eliminar_proceso(id)
        flash("Proceso productivo eliminado exitosamente", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("proc_prod.listar"))
