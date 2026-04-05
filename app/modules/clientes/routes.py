from flask import render_template, request, redirect, url_for, flash
from app.modules.clientes.forms import ClienteForm
from app.modules.clientes.service import ClienteService
from . import bp

servicio = ClienteService()

@bp.route("/")
def listar():
    page = request.args.get('page', 1, type=int)
    search_term = request.args.get('q', '')
    
    pagination = servicio.listar_paginados(page=page, per_page=10, search_term=search_term)
    
    return render_template("clientes/listar.html", 
                           pagination=pagination, 
                           search_term=search_term)

@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = ClienteForm()

    if form.validate_on_submit():
        try:
            data = {
                "nombres": form.nombres.data,
                "apellidos": form.apellidos.data,
                "email": form.email.data,
                "telefono": form.telefono.data,
                "calle_numero": form.calle_numero.data,
                "colonia": form.colonia.data,
                "ciudad": form.ciudad.data,
                "estado": form.estado.data,
                "codigo_postal": form.codigo_postal.data,
                "tipo": form.tipo.data
            }
            servicio.crear_cliente(data)
            flash("Cliente creado exitosamente.", "success")
            return redirect(url_for("clientes.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("clientes/crear.html", form=form)

@bp.route("/<int:id>")
def detalle(id):
    try:
        cliente = servicio.obtener_por_id(id)
        return render_template("clientes/detalle.html", cliente=cliente)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("clientes.listar"))

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        cliente = servicio.obtener_por_id(id)
        form = ClienteForm(obj=cliente)

        if form.validate_on_submit():
            try:
                data = {
                    "nombres": form.nombres.data,
                    "apellidos": form.apellidos.data,
                    "email": form.email.data,
                    "telefono": form.telefono.data,
                    "calle_numero": form.calle_numero.data,
                    "colonia": form.colonia.data,
                    "ciudad": form.ciudad.data,
                    "estado": form.estado.data,
                    "codigo_postal": form.codigo_postal.data,
                    "tipo": form.tipo.data
                }
                servicio.actualizar_cliente(id, data)
                flash("Cliente actualizado exitosamente.", "success")
                return redirect(url_for("clientes.detalle", id=id))
            except ValueError as e:
                flash(str(e), "danger")

        return render_template("clientes/crear.html", form=form, cliente=cliente)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("clientes.listar"))

@bp.route("/<int:id>/desactivar", methods=["POST"])
def desactivar(id):
    try:
        servicio.desactivar(id)
        flash("Cliente desactivado exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("clientes.listar"))

@bp.route("/<int:id>/activar", methods=["POST"])
def activar(id):
    try:
        servicio.activar(id)
        flash("Cliente activado exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("clientes.listar"))