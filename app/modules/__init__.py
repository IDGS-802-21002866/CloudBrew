from app.modules.usuarios import Usuario, Rol
from app.modules.proveedores import Proveedor
from app.modules.compras import Compra, DetalleCompra
from app.modules.materias_primas import MateriaPrima
from app.modules.unidades_medida import UnidadMedida
from app.modules.presentaciones import Presentacion
from app.modules.proc_prod.model import ProcesoProductivo
from app.modules.inventario_materias_primas import MovimientosMateriaPrima
from app.modules.recetas import Recetas, RecetaDetalle, ProcesosReceta

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
    "Recetas",
    "RecetaDetalle",
    "ProcesosReceta",
]
