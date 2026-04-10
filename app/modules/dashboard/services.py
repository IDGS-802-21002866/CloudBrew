
from app.modules.dashboard.repository import (
    obtener_producto_mas_vendido,
    obtener_producto_mas_producido,
    obtener_ventas_por_mes,
    obtener_mermas_por_mes
)


class DashboardService:

    def get_producto_mas_vendido(self):
        return obtener_producto_mas_vendido()

    def get_producto_mas_producido(self):
        return obtener_producto_mas_producido()

    def get_ventas_por_mes(self):
        return obtener_ventas_por_mes()

    def get_mermas_por_mes(self):
        return obtener_mermas_por_mes()