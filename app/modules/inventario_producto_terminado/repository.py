from sqlalchemy import case, func

from app import db
from app.modules.inventario_producto_terminado.model import MovimientosReceta
from app.modules.recetas.model import Recetas


def get_all_recetas_con_stock():
    stock_expr = func.coalesce(
        func.sum(
            case(
                (MovimientosReceta.tipo == "entrada", MovimientosReceta.cantidad),
                else_=-MovimientosReceta.cantidad,
            )
        ),
        0,
    )

    return (
        db.session.query(
            Recetas.id,
            Recetas.nombre,
            Recetas.descripcion,
            Recetas.cantidad_producida,
            stock_expr.label("stock_actual"),
        )
        .outerjoin(MovimientosReceta, MovimientosReceta.receta_id == Recetas.id)
        .filter(Recetas.activo == True)
        .group_by(
            Recetas.id,
            Recetas.nombre,
            Recetas.descripcion,
            Recetas.cantidad_producida,
        )
        .order_by(Recetas.nombre.asc())
        .all()
    )


def get_all_movimientos_by_receta_id(receta_id):
    return (
        MovimientosReceta.query.filter_by(receta_id=receta_id)
        .order_by(MovimientosReceta.fecha.desc(), MovimientosReceta.id.desc())
        .all()
    )


def get_receta_by_id(receta_id):
    return Recetas.query.get(receta_id)


def get_stock_actual_by_receta_id(receta_id):
    stock = (
        db.session.query(
            func.coalesce(
                func.sum(
                    case(
                        (
                            MovimientosReceta.tipo == "entrada",
                            MovimientosReceta.cantidad,
                        ),
                        else_=-MovimientosReceta.cantidad,
                    )
                ),
                0,
            )
        )
        .filter(MovimientosReceta.receta_id == receta_id)
        .scalar()
    )
    return float(stock or 0)
