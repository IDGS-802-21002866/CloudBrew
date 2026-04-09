from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import current_user
from . import bp
from .forms import PedidoForm, PedidoDetalleForm
from .service import PedidoService
from app.modules.clientes.service import ClienteService
from app.modules.recetas.service import RecetaService
from app.modules.recetas import repository as receta_repo

# Inicialización de servicios
pedido_service = PedidoService()
cliente_service = ClienteService()
receta_service = RecetaService()


@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")
    pagination = pedido_service.listar_paginados(
        page=page, per_page=10, search_term=search_term
    )
    return render_template(
        "pedidos/listar.html",
        pagination=pagination,
        search_term=search_term,
    )


@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = PedidoForm()
    detalle_form = PedidoDetalleForm()

    clientes_retail = [
        c for c in cliente_service.listar_clientes() if c.tipo.lower() == "retail"
    ]
    recetas = receta_service.listar_recetas(incluir_inactivas=False)
    detalle_form.receta_id.choices = [(r.id, r.nombre) for r in recetas]

    if "pedido_detalles" not in session:
        session["pedido_detalles"] = []

    # --- LÓGICA DE PRECARGA PARA EDICIÓN ---
    cliente_nombre_default = ""
    if "editando_pedido_id" in session:
        pedido_edit = pedido_service.obtener_por_id(session["editando_pedido_id"])
        # Si el formulario está vacío (primera carga), le ponemos el ID del cliente
        if not form.cliente_id.data:
            form.cliente_id.data = pedido_edit.cliente_id
        cliente_nombre_default = pedido_edit.cliente.nombre_completo

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "agregar_detalle":
            if detalle_form.validate_on_submit():
                receta = receta_repo.get_receta_by_id(detalle_form.receta_id.data)
                detalle = {
                    "receta_id": receta.id,
                    "receta_nombre": receta.nombre,
                    "cantidad_lotes": detalle_form.cantidad_lotes.data,
                    "total_unidades": detalle_form.cantidad_lotes.data
                    * receta.cantidad_producida,
                }
                session["pedido_detalles"].append(detalle)
                session.modified = True
                flash(f"{receta.nombre} agregado.", "success")

        elif action.startswith("quitar_detalle_"):
            idx = int(action.split("_")[-1])
            if 0 <= idx < len(session["pedido_detalles"]):
                session["pedido_detalles"].pop(idx)
                session.modified = True

        elif action == "crear_pedido":
            # Validamos que haya cliente y productos
            if form.cliente_id.data and session["pedido_detalles"]:
                data = {
                    "cliente_id": form.cliente_id.data,
                    "detalles": session["pedido_detalles"],
                }

                pedido_id = session.get("editando_pedido_id")
                if pedido_id:
                    # Lógica de actualización (Borrar y re-insertar detalles)
                    pedido = pedido_service.obtener_por_id(pedido_id)
                    from app.modules.pedidos.model import PedidoDetalle
                    from app import db

                    PedidoDetalle.query.filter_by(pedido_id=pedido.id).delete()

                    pedido.cliente_id = data["cliente_id"]
                    for d in data["detalles"]:
                        nuevo_d = PedidoDetalle(
                            pedido_id=pedido.id,
                            receta_id=d["receta_id"],
                            cantidad_lotes=d["cantidad_lotes"],
                            total_unidades=d["total_unidades"],
                        )
                        db.session.add(nuevo_d)
                    db.session.commit()
                    session.pop("editando_pedido_id", None)
                else:
                    pedido = pedido_service.crear_pedido(data, current_user.id)

                session["pedido_detalles"] = []
                session.modified = True
                flash("Pedido guardado con éxito.", "success")
                return redirect(url_for("pedidos.detalle", id=pedido.id))

    return render_template(
        "pedidos/crear.html",
        form=form,
        detalle_form=detalle_form,
        clientes_retail=clientes_retail,
        recetas=recetas,
        detalles=session["pedido_detalles"],
        cliente_nombre_default=cliente_nombre_default,
    )
    form = PedidoForm()
    detalle_form = PedidoDetalleForm()

    clientes_retail = [
        c for c in cliente_service.listar_clientes() if c.tipo.lower() == "retail"
    ]
    recetas = receta_service.listar_recetas(incluir_inactivas=False)
    detalle_form.receta_id.choices = [(r.id, r.nombre) for r in recetas]

    if "pedido_detalles" not in session:
        session["pedido_detalles"] = []

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "agregar_detalle":
            if detalle_form.validate_on_submit():
                receta = receta_repo.get_receta_by_id(detalle_form.receta_id.data)
                detalle = {
                    "receta_id": receta.id,
                    "receta_nombre": receta.nombre,
                    "cantidad_lotes": detalle_form.cantidad_lotes.data,
                    "total_unidades": detalle_form.cantidad_lotes.data
                    * receta.cantidad_producida,
                }
                session["pedido_detalles"].append(detalle)
                session.modified = True
                flash(f"{receta.nombre} agregado.", "success")

        elif action.startswith("quitar_detalle_"):
            idx = int(action.split("_")[-1])
            if 0 <= idx < len(session["pedido_detalles"]):
                session["pedido_detalles"].pop(idx)
                session.modified = True

        elif action == "crear_pedido":
            if form.validate_on_submit() and session["pedido_detalles"]:
                data = {
                    "cliente_id": form.cliente_id.data,
                    "detalles": session["pedido_detalles"],
                }

                # Si estamos editando uno existente
                pedido_id = session.get("editando_pedido_id")
                if pedido_id:
                    # Lógica para actualizar (borrar detalles viejos y poner nuevos)
                    pedido = pedido_service.obtener_por_id(pedido_id)
                    # Limpiamos detalles viejos
                    from app.modules.pedidos.model import PedidoDetalle

                    PedidoDetalle.query.filter_by(pedido_id=pedido.id).delete()

                    # Actualizamos cabecera
                    pedido.cliente_id = data["cliente_id"]
                    # Re-usamos la lógica de guardar detalles del service
                    for d in data["detalles"]:
                        nuevo_d = PedidoDetalle(
                            pedido_id=pedido.id,
                            receta_id=d["receta_id"],
                            cantidad_lotes=d["cantidad_lotes"],
                            total_unidades=d["total_unidades"],
                        )
                        from app import db

                        db.session.add(nuevo_d)
                    db.session.commit()
                    session.pop("editando_pedido_id", None)
                else:
                    pedido = pedido_service.crear_pedido(data, current_user.id)

                session["pedido_detalles"] = []
                session.modified = True
                flash("Pedido guardado correctamente.", "success")
                return redirect(url_for("pedidos.detalle", id=pedido.id))

    return render_template(
        "pedidos/crear.html",
        form=form,
        detalle_form=detalle_form,
        clientes_retail=clientes_retail,
        recetas=recetas,
        detalles=session["pedido_detalles"],
    )


@bp.route("/<int:id>/editar")
def editar(id):
    pedido = pedido_service.obtener_por_id(id)
    if pedido.estado != "Pendiente":
        flash("Solo se pueden editar pedidos pendientes.", "warning")
        return redirect(url_for("pedidos.detalle", id=id))

    # PASO CLAVE: Cargar los datos del pedido viejo a la sesión
    session["pedido_detalles"] = []
    for d in pedido.detalles:
        session["pedido_detalles"].append(
            {
                "receta_id": d.receta_id,
                "receta_nombre": d.receta.nombre,
                "cantidad_lotes": d.cantidad_lotes,
                "total_unidades": d.total_unidades,
            }
        )
    session["editando_pedido_id"] = id
    session.modified = True

    # Redirigimos al formulario de crear, pero ya con la sesión llena
    flash("Editando pedido existente.", "info")
    return redirect(url_for("pedidos.crear"))


@bp.route("/<int:id>")
def detalle(id):
    pedido = pedido_service.obtener_por_id(id)
    return render_template("pedidos/detalle.html", pedido=pedido)


# --- ESTAS SON LAS RUTAS QUE TE FALTABAN PARA QUE EL DETALLE NO TRUENE ---


@bp.route("/<int:id>/cancelar", methods=["POST"])
def cancelar(id):
    try:
        pedido_service.cancelar_pedido(id)
        flash("Pedido cancelado exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("pedidos.listar"))
