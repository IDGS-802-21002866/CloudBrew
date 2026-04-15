from flask import Blueprint

from app.modules.producto_venta.model import ProductoVenta

__all__ = ["ProductoVenta"]
bp = Blueprint(
    "producto_venta",
    __name__,
    url_prefix="/producto_venta",
    template_folder="templates",
)

from app.modules.producto_venta import routes  # noqa: E402, F401
