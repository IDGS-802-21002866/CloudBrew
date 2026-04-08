from flask import Blueprint
from .model import Pedido, PedidoDetalle

bp = Blueprint(
    "pedidos",
    __name__,
    url_prefix="/pedidos",
    template_folder="templates",
)

from . import routes

__all__ = ["Pedido", "PedidoDetalle"]
