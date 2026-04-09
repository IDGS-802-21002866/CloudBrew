from app.modules.pedidos import repository as pedido_repo
from app.modules.pedidos.model import Pedido, PedidoDetalle
from app.modules.clientes.service import ClienteService
from app.modules.recetas.service import RecetaService
from app.modules.produccion.service import ProduccionService


class PedidoService:
    def listar_paginados(self, page=1, per_page=10, search_term=None):
        return pedido_repo.get_paginated_pedidos(page, per_page, search_term)

    def obtener_por_id(self, pedido_id):
        pedido = pedido_repo.get_pedido_by_id(pedido_id)
        if not pedido:
            raise ValueError("Pedido no encontrado.")
        return pedido

    def crear_pedido(self, data, usuario_id):
        cliente_id = data.get("cliente_id")
        if not cliente_id:
            raise ValueError("Debe seleccionar un cliente.")

        cliente_service = ClienteService()
        cliente = cliente_service.obtener_por_id(cliente_id)
        if cliente.tipo.lower() != "retail":
            raise ValueError("Solo se permiten pedidos para clientes retail.")

        detalles_data = data.get("detalles", [])
        if not detalles_data:
            raise ValueError("Debe agregar al menos un producto al pedido.")

        receta_service = RecetaService()
        detalles = []

        for detalle in detalles_data:
            receta_id = detalle.get("receta_id")
            cantidad_lotes = detalle.get("cantidad_lotes")

            if not receta_id or not cantidad_lotes:
                raise ValueError("Datos de detalle incompletos.")

            receta = receta_service.obtener_receta(receta_id)
            total_unidades = float(cantidad_lotes) * receta.cantidad_producida

            detalles.append(
                {
                    "receta_id": receta_id,
                    "cantidad_lotes": cantidad_lotes,
                    "total_unidades": total_unidades,
                }
            )

        # Crear pedido y detalles (flush, sin commit)
        pedido = pedido_repo.create_pedido(cliente_id, detalles)

        # Crear orden de produccion por cada detalle y registrar relacion transaccional
        produccion_service = ProduccionService()
        for detalle in detalles:
            produccion = produccion_service.crear_produccion(
                {
                    "id_receta": detalle["receta_id"],
                    "cantidad": detalle["cantidad_lotes"],
                }
            )
            pedido_repo.create_pedido_produccion(pedido.id, produccion.id_produccion)

        pedido_repo.commit()
        return pedido

    def cancelar_pedido(self, pedido_id):
        pedido = self.obtener_por_id(pedido_id)
        if pedido.estado != "Pendiente":
            raise ValueError("Solo se pueden cancelar pedidos en estado 'Pendiente'.")

        producciones = pedido_repo.get_producciones_by_pedido(pedido_id)
        produccion_service = ProduccionService()
        for pedido_produccion in producciones:
            produccion_service.cancelar_produccion_forzada(
                pedido_produccion.id_produccion
            )

        pedido_repo.update_pedido_estado(pedido, "Cancelado")
        return pedido
