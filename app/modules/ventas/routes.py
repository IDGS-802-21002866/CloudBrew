from flask import Blueprint, render_template, redirect, request, url_for, flash

from app.modules.ventas.service import VentaService
from app.shared.exceptions import EntidadNoEncontradaError
from . import bp

venta_service = VentaService()


@bp.route("/")
def listar():
    page=request.args.get("page", 1, type=int)
    ventas = venta_service.listar_ventas_paginadas(page=page, per_page=10)
    return render_template("ventas/listar.html", pagination=ventas)


@bp.route("/<int:id>")
def detalle(id):
    try:
        venta = venta_service.obtener_venta(id)
    except EntidadNoEncontradaError:
        flash("Venta no encontrada", "error")
        return redirect(url_for("ventas.listar"))
    return render_template("ventas/detalle.html", venta=venta)


@bp.route("/<int:id>/cancelar", methods=["POST"])
def cancelar(id):
    try:
        venta_service.cancelar_venta(id)
        flash("Venta cancelada exitosamente", "success")
    except EntidadNoEncontradaError as e:
        flash(f"Error: {str(e)}", "error")
    except ValueError as e:
        flash(f"Error: {str(e)}", "error")
    except Exception as e:
        flash(f"Error inesperado: {str(e)}", "error")

    return redirect(url_for("ventas.detalle", id=id))
