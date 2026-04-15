from app.modules.dashboard.model import (
    ProductoMasVendido,
    ProductoMasProducido,
    UtilidadProducto,
    VentasPorMes,
    MermasPorMes,
)


def obtener_producto_mas_vendido():
    return ProductoMasVendido.query.order_by(
        ProductoMasVendido.total_vendido.desc()
    ).first()


def obtener_producto_mas_producido():
    return ProductoMasProducido.query.order_by(
        ProductoMasProducido.total_producido.desc()
    ).first()
# app/modules/dashboard/repository.py

def obtener_ventas_por_mes():
    return VentasPorMes.query.order_by(
        VentasPorMes.anio.desc(),
        VentasPorMes.mes.desc()
    ).all()


def obtener_mermas_por_mes():
    return MermasPorMes.query.order_by(
        MermasPorMes.anio.desc(),
        MermasPorMes.mes.desc()
    ).all()
    
def  query_utilidad_productos():
        return (
            UtilidadProducto.query
            .order_by(UtilidadProducto.utilidad.desc())
            .all()
        )