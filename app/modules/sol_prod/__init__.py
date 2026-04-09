from flask import Blueprint

from app.modules.sol_prod.model import Pedido,DetallePedido,PedidoProduccion

__all__ = ["Pedido", "DetallePedido","PedidoProduccion"]
bp = Blueprint("sol_prod", __name__, url_prefix="", template_folder="templates/sol_prod")

from . import routes
