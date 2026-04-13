from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import current_user
from . import bp
from .forms import PedidoForm, PedidoDetalleForm
from .service import PedidoService
from app.modules.clientes.service import ClienteService
from app.modules.recetas.service import RecetaService
from app.modules.recetas import repository as receta_repo
from app.shared.decorators import login_required
from app.modules.inventario_materias_primas.service import (
    InventarioMateriasPrimasService,
)

# Inicialización de servicios
pedido_service = PedidoService()
cliente_service = ClienteService()
receta_service = RecetaService()
inventario_service = InventarioMateriasPrimasService()


@login_required
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


@login_required
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
        if not form.cliente_id.data:
            form.cliente_id.data = pedido_edit.cliente_id
        cliente_nombre_default = pedido_edit.cliente.nombre_completo

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "agregar_detalle":
            if detalle_form.validate_on_submit():
                receta = receta_repo.get_receta_by_id(detalle_form.receta_id.data)
                cantidad_nueva = detalle_form.cantidad_lotes.data

                detalle_existente = next(
                    (
                        d
                        for d in session["pedido_detalles"]
                        if d["receta_id"] == receta.id
                    ),
                    None,
                )

                cantidad_total = cantidad_nueva
                if detalle_existente:
                    cantidad_total += detalle_existente["cantidad_lotes"]

                try:
                    for detalle in receta.detalle:
                        cantidad_necesaria = detalle.cantidad * int(cantidad_total)
                        stock_disponible = (
                            inventario_service.obtener_stock_actual_materia_prima(
                                detalle.materia_prima_id
                            )
                        )
                        if stock_disponible < cantidad_necesaria:
                            raise ValueError(
                                f"Stock insuficiente para '{detalle.materia_prima.nombre}'. "
                                f"Necesario: {cantidad_necesaria}, Disponible: {stock_disponible}"
                            )
                except ValueError as e:
                    flash(str(e), "danger")
                    return redirect(url_for("pedidos.crear"))

                if detalle_existente:
                    detalle_existente["cantidad_lotes"] = cantidad_total
                    detalle_existente["total_unidades"] = (
                        cantidad_total * receta.cantidad_producida
                    )
                    flash(f"{receta.nombre} actualizado.", "success")
                else:
                    session["pedido_detalles"].append(
                        {
                            "receta_id": receta.id,
                            "receta_nombre": receta.nombre,
                            "cantidad_lotes": cantidad_nueva,
                            "total_unidades": cantidad_nueva
                            * receta.cantidad_producida,
                        }
                    )
                    flash(f"{receta.nombre} agregado.", "success")

                session.modified = True

        elif action.startswith("quitar_detalle_"):
            idx = int(action.split("_")[-1])
            if 0 <= idx < len(session["pedido_detalles"]):
                session["pedido_detalles"].pop(idx)
                session.modified = True

        elif action == "crear_pedido":
            if form.cliente_id.data and session["pedido_detalles"]:
                data = {
                    "cliente_id": form.cliente_id.data,
                    "detalles": session["pedido_detalles"],
                }

                try:
                    pedido_id = session.get("editando_pedido_id")
                    if pedido_id:
                        from app.modules.pedidos.model import PedidoDetalle
                        from app import db

                        pedido = pedido_service.obtener_por_id(pedido_id)
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
                except ValueError as e:
                    flash(str(e), "danger")

    return render_template(
        "pedidos/crear.html",
        form=form,
        detalle_form=detalle_form,
        clientes_retail=clientes_retail,
        recetas=recetas,
        detalles=session["pedido_detalles"],
        cliente_nombre_default=cliente_nombre_default,
    )


@login_required
@bp.route("/<int:id>/editar")
def editar(id):
    try:
        pedido = pedido_service.obtener_por_id(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("pedidos.listar"))
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


@login_required
@bp.route("/<int:id>")
def detalle(id):
    try:
        pedido = pedido_service.obtener_por_id(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("pedidos.listar"))
    return render_template("pedidos/detalle.html", pedido=pedido)


# --- ESTAS SON LAS RUTAS QUE TE FALTABAN PARA QUE EL DETALLE NO TRUENE ---


@login_required
@bp.route("/<int:id>/cancelar", methods=["POST"])
def cancelar(id):
    try:
        pedido_service.cancelar_pedido(id)
        flash("Pedido cancelado exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("pedidos.listar"))
