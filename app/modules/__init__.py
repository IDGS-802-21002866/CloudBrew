from app.modules.usuarios import Usuario, Rol
from app.modules.proveedores import Proveedor
from app.modules.compras import Compra, DetalleCompra
from app.modules.materias_primas import MateriaPrima
from app.modules.unidades_medida import UnidadMedida
from app.modules.presentaciones import Presentacion
from app.modules.proc_prod.model import ProcesoProductivo
from app.modules.inventario_materias_primas import MovimientosMateriaPrima
from app.modules.inventario_producto_terminado import MovimientosReceta
from app.modules.recetas import Recetas, RecetaDetalle, ProcesosReceta
from app.modules.sol_prod.model import Pedido, DetallePedido, PedidoProduccion
from app.modules.lotes.model import LoteProduccion
from app.modules.produccion.model import Produccion, ProduccionProceso
from app.modules.pedidos import Pedido, PedidoDetalle

#  Agregar nuevos modelos aquí y luego importarlos en __all__ para que estén disponibles en toda la aplicación
__all__ = [
    "Usuario",
    "Rol",
    "Proveedor",
    "Compra",
    "ProcesoProductivo",
    "DetalleCompra",
    "MateriaPrima",
    "UnidadMedida",
    "Presentacion",
    "ProcesoProductivo",
    "MovimientosMateriaPrima",
    "MovimientosReceta",
    "Recetas",
    "RecetaDetalle",
    "ProcesosReceta",
    "Pedido",
    "DetallePedido",
    "PedidoProduccion",
    "LoteProduccion",
    "Produccion",
    "ProduccionProceso" "Pedido",
    "PedidoDetalle",
]
