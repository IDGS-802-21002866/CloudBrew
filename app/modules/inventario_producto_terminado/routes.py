from flask import flash, redirect, render_template, request, url_for

from . import bp
from app.modules.inventario_producto_terminado.service import (
    InventarioProductoTerminadoService,
)
from app.modules.produccion.service import ProduccionService
from app.shared.decorators import verificar_rol_o_denegar


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin", "almacen", "ventas")


servicio = InventarioProductoTerminadoService()
produccion_service = ProduccionService()


@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    inventario = servicio.listar_recetas_con_stock_pag(page, per_page=10)
    return render_template(
        "inventario_producto_terminado/listar.html", pagination=inventario
    )


@bp.route("/<int:id>")
def detalle(id):
    try:
        receta = servicio.obtener_receta(id)
        movimientos = servicio.listar_movimientos_receta(id)
        stock_actual = servicio.obtener_stock_actual_receta(id)
        return render_template(
            "inventario_producto_terminado/detalle.html",
            receta=receta,
            movimientos=movimientos,
            stock_actual=stock_actual,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("inventario_producto_terminado.listar"))


@bp.route("/solicitar_produccion")
def solicitar_produccion():
    page = request.args.get("page", 1, type=int)
    recetas_bajo_stock = servicio.listar_recetas_bajo_stock_pag(page, per_page=10)
    return render_template(
        "inventario_producto_terminado/solicitar_produccion.html",
        pagination=recetas_bajo_stock,
    )


@bp.route("/solicitar_produccion/<int:receta_id>", methods=["POST"])
def crear_solicitud_produccion(receta_id):
    cantidad = request.form.get("cantidad", 1, type=int)
    try:
        receta = servicio.obtener_receta(receta_id)
        stock_actual = servicio.obtener_stock_actual_receta(receta_id)
        cantidad_producida = float(receta.cantidad_producida or 0)
        if cantidad_producida > 0 and stock_actual >= cantidad_producida:
            flash(
                "Esta receta tiene stock suficiente. No se puede solicitar producción.",
                "warning",
            )
            return redirect(
                url_for("inventario_producto_terminado.solicitar_produccion")
            )

        produccion_service.crear_produccion(
            {
                "id_receta": receta_id,
                "cantidad": cantidad,
            }
        )
        flash(
            f"Orden de producción creada para '{receta.nombre}' ({cantidad} lote{'s' if cantidad > 1 else ''}).",
            "success",
        )
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("inventario_producto_terminado.solicitar_produccion"))
