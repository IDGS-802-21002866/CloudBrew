from app import db
from app.modules.compras.model import DetalleCompra, Compra
from app.modules.presentaciones.model import Presentacion


def get_costo_promedio_materia_prima(materia_prima_id):
    """
    Calcula el costo promedio por unidad base (kg/litro) de una materia prima,
    basado en todas las compras confirmadas.

    Formula: SUM(precio_unitario * cantidad) / SUM(cantidad * cantidad_equivalente)
    """
    resultado = (
        db.session.query(
            db.func.sum(DetalleCompra.precio_unitario * DetalleCompra.cantidad)
            / db.func.sum(DetalleCompra.cantidad * Presentacion.cantidad_equivalente)
        )
        .join(Presentacion, DetalleCompra.presentacion_id == Presentacion.id)
        .join(Compra, DetalleCompra.compra_id == Compra.id)
        .filter(
            DetalleCompra.materia_prima_id == materia_prima_id,
            Compra.fecha_compra.isnot(None),
            Compra.cancelada == False,
            DetalleCompra.precio_unitario > 0,
        )
        .scalar()
    )
    return float(resultado) if resultado else 0.0


def get_all_materias_primas_activas():
    from app.modules.materias_primas.model import MateriaPrima

    return MateriaPrima.query.filter_by(activo=True).order_by(MateriaPrima.nombre).all()


def get_all_recetas_activas():
    from app.modules.recetas.model import Recetas

    return Recetas.query.filter_by(activo=True).order_by(Recetas.nombre).all()
