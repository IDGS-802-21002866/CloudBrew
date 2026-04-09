from app.modules.pedidos.model import Pedido, PedidoDetalle
from app.modules.sol_prod.model import PedidoProduccion
from app import db


def crear_pedido(form):
    try:
        pedido = Pedido(
            cliente_id=form.cliente_id.data,
            fecha_registro=form.fecha_registro.data,
            estado=form.estado.data,
        )

        db.session.add(pedido)
        db.session.commit()

        return pedido

    except Exception:
        db.session.rollback()
        raise ValueError(
            "No se pudo crear el pedido. Verifica los datos proporcionados."
        )


def crear_detalle_pedido(form, pedido_id):
    try:
        detalle = PedidoDetalle(
            pedido_id=pedido_id,
            receta_id=form.receta_id.data,
            cantidad_lotes=form.cantidad_lotes.data,
        )

        db.session.add(detalle)
        db.session.commit()

        return detalle

    except Exception:
        db.session.rollback()
        raise ValueError(
            "No se pudo agregar el detalle del pedido. Verifica la receta y cantidad."
        )


def vincular_pedido_produccion(form):
    try:
        relacion = PedidoProduccion(
            id_pedido=form.id_pedido.data, id_produccion=form.id_produccion.data
        )

        db.session.add(relacion)
        db.session.commit()

        return relacion

    except Exception:
        db.session.rollback()
        raise ValueError("No se pudo vincular el pedido con la producción.")


def actualizar_pedido(form, pedido_id):
    try:
        pedido = Pedido.query.get(pedido_id)

        if not pedido:
            raise ValueError("El pedido no existe.")

        pedido.cliente_id = form.cliente_id.data
        pedido.fecha_registro = form.fecha_registro.data
        pedido.estado = form.estado.data

        db.session.commit()

        return pedido

    except ValueError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise ValueError("No se pudo actualizar el pedido.")


def actualizar_detalle_pedido(form, id_detalle):
    try:
        detalle = PedidoDetalle.query.get(id_detalle)

        if not detalle:
            raise ValueError("El detalle del pedido no existe.")

        if form.cantidad_lotes.data <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")

        detalle.receta_id = form.receta_id.data
        detalle.cantidad_lotes = form.cantidad_lotes.data

        db.session.commit()

        return detalle

    except ValueError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise ValueError("No se pudo actualizar el detalle del pedido.")


def actualizar_pedido_produccion(form, id_relacion):
    try:
        relacion = PedidoProduccion.query.get(id_relacion)

        if not relacion:
            raise ValueError("La relación pedido-producción no existe.")

        relacion.id_pedido = form.id_pedido.data
        relacion.id_produccion = form.id_produccion.data

        db.session.commit()

        return relacion

    except ValueError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise ValueError("No se pudo actualizar la relación pedido-producción.")


def cancelar_pedido(pedido_id):
    try:
        pedido = Pedido.query.get(pedido_id)

        if not pedido:
            raise ValueError("El pedido no existe.")

        if pedido.estado == "cancelado":
            raise ValueError("El pedido ya está cancelado.")

        pedido.estado = "cancelado"

        db.session.commit()

        return pedido

    except ValueError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise ValueError("No se pudo cancelar el pedido.")


def eliminar_detalle_pedido(id_detalle):
    try:
        detalle = PedidoDetalle.query.get(id_detalle)

        if not detalle:
            raise ValueError("El detalle del pedido no existe.")

        db.session.delete(detalle)
        db.session.commit()

        return True

    except ValueError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise ValueError("No se pudo eliminar el detalle del pedido.")


def get_pedidos():
    try:
        return Pedido.query.all()
    except Exception:
        return ValueError("Ocurrió un error al obtener los pedidos de producción.")


def get_pedidos_by_id(id):
    try:
        return Pedido.query.filter_by(id=id)
    except Exception:
        return ValueError("Ocurrió un error al obtener los pedidos de producción.")


def get_detalles_pedido_by_pedido(id):
    try:
        return PedidoDetalle.query.filter_by(pedido_id=id)
    except Exception:
        return ValueError(
            "Ocurrió un error al obtener los detalles del pedido de producción."
        )


def get_pedidos_prod():
    try:
        return PedidoProduccion.query.all()
    except Exception:
        return ValueError("Ocurrió un error el pedido de producción.")
