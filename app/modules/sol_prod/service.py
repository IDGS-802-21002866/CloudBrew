from app import db
from app.modules.sol_prod.repository import (
    crear_pedido,
    crear_detalle_pedido,
    actualizar_pedido,
    eliminar_detalle_pedido,
    cancelar_pedido,
    get_detalles_pedido_by_pedido,
    get_pedidos,
    get_pedidos_by_id,
    get_pedidos_prod
)


class sol_prod_service:

    def insertar(self,form_pedido, lista_detalles_forms):
        try:
            pedido = crear_pedido(form_pedido)

            for form_detalle in lista_detalles_forms:
                if not form_detalle.validate():
                    raise ValueError("Uno de los detalles tiene datos inválidos.")

                crear_detalle_pedido(form_detalle, pedido.id_pedido)

            return pedido

        except ValueError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise ValueError("No se pudo registrar la solicitud de producción.")
    
    def modificar(self,id_pedido, form_pedido, lista_detalles_forms):
        try:
            pedido = actualizar_pedido(form_pedido, id_pedido)

            for detalle in pedido.detalles:
                eliminar_detalle_pedido(detalle.id_detalle_pedido)

            for form_detalle in lista_detalles_forms:
                if not form_detalle.validate():
                    raise ValueError("Uno de los detalles tiene datos inválidos.")

                crear_detalle_pedido(form_detalle, pedido.id_pedido)

            return pedido

        except ValueError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise ValueError("No se pudo modificar la solicitud de producción.")
    
    def eliminar(self,id_pedido):
        try:
            pedido = cancelar_pedido(id_pedido)
            return pedido

        except ValueError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise ValueError("No se pudo cancelar la solicitud de producción.")
    
    def listar_pedidos(self):
        return get_pedidos()

    def obtener_pedido_por_id(self, id_pedido):
        return get_pedidos_by_id(id_pedido)

    def obtener_detalles_de_pedido(self, id_pedido):
        return get_detalles_pedido_by_pedido(id_pedido)

    def listar_pedidos_produccion_general(self):
        return get_pedidos_prod()