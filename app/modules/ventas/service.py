from app.modules.ventas.repository import VentaRepository
from app.shared.exceptions import EntidadNoEncontradaError


class VentaService:
    def __init__(self):
        self.repository = VentaRepository()

    def listar_ventas(self):
        return self.repository.get_all_ventas()

    def obtener_venta(self, id_venta):
        venta = self.repository.get_venta_by_id(id_venta)
        if not venta:
            raise EntidadNoEncontradaError(f"Venta {id_venta} no encontrada")
        return venta

    def cancelar_venta(self, id_venta):
        venta = self.obtener_venta(id_venta)

        if venta.cancelada:
            raise ValueError("La venta ya está cancelada")

        return self.repository.update_venta(id_venta, cancelada=True)
