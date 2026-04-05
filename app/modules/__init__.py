from app.modules.usuarios import Usuario
from app.modules.proveedores import Proveedor
from app.modules.proc_prod.model import ProcesoProductivo

#  Agregar nuevos modelos aquí y luego importarlos en __all__ para que estén disponibles en toda la aplicación
__all__ = ["Usuario", "Proveedor", "ProcesoProductivo"]
