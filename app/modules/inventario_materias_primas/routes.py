from flask import flash, redirect, render_template, request, url_for

from . import bp
from app.modules.compras.service import ComprasService
from app.modules.inventario_materias_primas.service import (
    InventarioMateriasPrimasService,
)
from app.shared.decorators import verificar_rol_o_denegar


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin", "almacen", "compras")


servicio = InventarioMateriasPrimasService()
compras_service = ComprasService()


@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")

    pagination = servicio.listar_materias_primas_paginadas(
        page=page, per_page=10, search_term=search_term
    )

    return render_template(
        "inventario_materias_primas/listar.html",
        pagination=pagination,
        search_term=search_term,
    )


@bp.route("/<int:id>")
def detalle(id):
    try:
        materia_prima = servicio.obtener_materia_prima(id)
        movimientos = servicio.listar_movimientos_materia_prima(id)
        stock_actual = servicio.obtener_stock_actual_materia_prima(id)
        return render_template(
            "inventario_materias_primas/detalle.html",
            materia_prima=materia_prima,
            movimientos=movimientos,
            stock_actual=stock_actual,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("inventario_materias_primas.listar"))


# app/modules/inventario_materias_primas/routes.py


@bp.route("/solicitar", defaults={"id": None}, methods=["GET", "POST"])
@bp.route("/solicitar/<int:id>", methods=["GET", "POST"])
def solicitar(id):
    materia = None
    materias = []
    unidad_hint = "unidades"

    if id:
        materia = servicio.obtener_materia_prima(id)
        stock_actual = servicio.obtener_stock_actual_materia_prima(id)
        if stock_actual > 0:
            # Verificar si está por encima del mínimo (2 lotes)
            from app.modules.inventario_materias_primas.repository import (
                get_all_materias_primas_con_stock,
            )

            items = get_all_materias_primas_con_stock(page=1, per_page=1000).items
            item_data = next((i for i in items if i.id == id), None)
            if item_data:
                stock_min_base = float(item_data.max_receta or 0) * 2
                stock_act_base = float(item_data.stock_actual_base or 0)
                if stock_act_base >= stock_min_base:
                    flash(
                        "Esta materia prima tiene stock suficiente. No se puede solicitar compra.",
                        "warning",
                    )
                    return redirect(url_for("inventario_materias_primas.listar"))
        unidad_hint = (
            materia.tipo_medida.unidad_base if materia.tipo_medida else "unidades"
        )
    else:
        # Solo listar materias primas con bajo o nulo stock
        all_items = servicio.listar_materias_primas_paginadas(per_page=1000).items
        materias = [
            item
            for item in all_items
            if item.get("estado_stock") in ("bajo_stock", "sin_stock")
        ]

    if request.method == "POST":
        materia_id = id or request.form.get("materia_prima_id")
        cantidad = request.form.get("cantidad")

        try:
            compras_service.crear_solicitud_compra(
                materia_prima_id=materia_id,
                cantidad=float(cantidad),
                origen="almacen",
            )
            flash("Solicitud de compra creada exitosamente.", "success")
            return redirect(url_for("inventario_materias_primas.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "inventario_materias_primas/solicitar.html",
        materia=materia,
        materias=materias,
        unidad_hint=unidad_hint,
    )
