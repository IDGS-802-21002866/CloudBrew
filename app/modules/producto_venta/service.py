from flask_login import current_user

from app.modules.presentaciones.service import PresentacionService
from app.modules.producto_venta import repository
from app.modules.producto_venta.model import ProductoVenta
from app.modules.recetas.service import RecetaService
from app.shared.exceptions import ValidacionNegocioException

receta_service = RecetaService()
presentacion_service = PresentacionService()


class ProductoVentaService:
    def listar_productos_venta(self):
        return repository.get_all_producto_venta()

    def listar_paginados(self, page=1, per_page=10, search_term=None):
        """Obtiene productos paginados con búsqueda opcional."""
        return repository.get_productos_venta_paginados(
            page=page, per_page=per_page, search_term=search_term
        )

    def listar_por_tipo(self, tipo):
        return repository.get_producto_venta_by_tipo(tipo)

    def listar_activos(self):
        return repository.get_activos_producto_venta()

    def obtener_producto_venta(self, id):
        producto = repository.get_producto_venta_by_id(id)
        if not producto:
            raise ValueError("Producto de venta no encontrado.")
        return producto

    def crear_producto_venta(self, data):
        receta_id = data.get("receta_id")
        presentacion_id = data.get("presentacion_id")

        receta = receta_service.obtener_receta(receta_id)
        presentacion = presentacion_service.obtener_por_id(presentacion_id)

        precio = data.get("precio_venta")
        if not precio:
            raise ValidacionNegocioException("El precio de venta es obligatorio.")

        nuevo = ProductoVenta(
            receta_id=receta.id,
            presentacion_id=presentacion.id,
            nombre=data.get("nombre", "").strip(),
            descripcion=data.get("descripcion"),
            tipo=data.get("tipo", "web"),
            cantidad_unidades=int(presentacion.cantidad_equivalente),
            precio_venta=float(precio),
            activo=True,
            usuario_id=current_user.id if current_user.is_authenticated else None,
        )
        return repository.create_producto_venta(nuevo)

    def actualizar_producto_venta(self, id, data):
        producto = self.obtener_producto_venta(id)
        presentacion_id = data.get("presentacion_id")
        presentacion = presentacion_service.obtener_por_id(presentacion_id)

        producto.receta_id = data.get("receta_id")
        producto.presentacion_id = presentacion.id
        producto.nombre = data.get("nombre", "").strip()
        producto.descripcion = data.get("descripcion")
        producto.tipo = data.get("tipo", "web")
        producto.cantidad_unidades = int(presentacion.cantidad_equivalente)
        producto.precio_venta = float(data.get("precio_venta"))
        producto.usuario_id = (
            current_user.id if current_user.is_authenticated else producto.usuario_id
        )
        return repository.update_producto_venta(producto)

    def desactivar_producto_venta(self, id):
        producto = self.obtener_producto_venta(id)
        if not producto.activo:
            raise ValidacionNegocioException("El producto ya está desactivado.")
        return repository.deactivate_producto_venta(producto)

    def activar_producto_venta(self, id):
        producto = self.obtener_producto_venta(id)
        if producto.activo:
            raise ValidacionNegocioException("El producto ya está activo.")
        return repository.activate_producto_venta(producto)
