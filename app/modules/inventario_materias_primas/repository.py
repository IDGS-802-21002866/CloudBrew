from sqlalchemy import case, func

from app import db
from app.modules.inventario_materias_primas.model import MovimientosMateriaPrima
from app.modules.materias_primas.model import MateriaPrima


def get_all_materias_primas_con_stock():
    stock_expr = func.coalesce(
        func.sum(
            case(
                (
                    MovimientosMateriaPrima.tipo == "entrada",
                    MovimientosMateriaPrima.cantidad,
                ),
                else_=-MovimientosMateriaPrima.cantidad,
            )
        ),
        0,
    )

    return (
        db.session.query(
            MateriaPrima.id,
            MateriaPrima.nombre,
            MateriaPrima.tipo_medida_id,
            MateriaPrima.stock_minimo,
            stock_expr.label("stock_actual"),
        )
        .outerjoin(
            MovimientosMateriaPrima,
            MovimientosMateriaPrima.materia_prima_id == MateriaPrima.id,
        )
        .group_by(
            MateriaPrima.id,
            MateriaPrima.nombre,
            MateriaPrima.tipo_medida_id,
            MateriaPrima.stock_minimo,
        )
        .order_by(MateriaPrima.nombre.asc())
        .all()
    )


def get_all_movimientos_by_materia_prima_id(materia_prima_id):
    return (
        MovimientosMateriaPrima.query.filter_by(materia_prima_id=materia_prima_id)
        .order_by(
            MovimientosMateriaPrima.fecha.desc(), MovimientosMateriaPrima.id.desc()
        )
        .all()
    )


def get_materia_prima_by_id(materia_prima_id):
    return MateriaPrima.query.get(materia_prima_id)


def get_stock_actual_by_materia_prima_id(materia_prima_id):
    stock = (
        db.session.query(
            func.coalesce(
                func.sum(
                    case(
                        (
                            MovimientosMateriaPrima.tipo == "entrada",
                            MovimientosMateriaPrima.cantidad,
                        ),
                        else_=-MovimientosMateriaPrima.cantidad,
                    )
                ),
                0,
            )
        )
        .filter(MovimientosMateriaPrima.materia_prima_id == materia_prima_id)
        .scalar()
    )
    return float(stock or 0)
