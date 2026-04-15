from math import ceil

from app import db
from app.modules.pedidos import repository as pedido_repo
from app.modules.pedidos.model import Pedido, PedidoDetalle
from app.modules.clientes.service import ClienteService
from app.modules.producto_venta.service import ProductoVentaService
from app.modules.produccion.service import ProduccionService
from app.modules.compras.repository import create_solicitud
from flask_login import current_user


class PedidoService:
    def listar_paginados(self, page=1, per_page=10, search_term=None):
        return pedido_repo.get_paginated_pedidos(page, per_page, search_term)

    def listar_paginado_terminados(self, page=1, per_page=10, search_term=None):
        return pedido_repo.get_paginated_pedidos_terminados(page, per_page, search_term)

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

        producto_venta_service = ProductoVentaService()
        detalles = []
        total_pedido = 0.0

        solicitudes_agrupadas = {}
        for detalle in detalles_data:
            producto_venta_id = detalle.get("producto_venta_id")
            cantidad = int(detalle.get("cantidad") or 0)

            if not producto_venta_id or not cantidad:
                raise ValueError("Datos de detalle incompletos.")

            producto_venta = producto_venta_service.obtener_producto_venta(
                producto_venta_id
            )
            receta = producto_venta.receta

            total_unidades = cantidad * producto_venta.cantidad_unidades
            cantidad_lotes = ceil(total_unidades / receta.cantidad_producida)
            precio_unitario = float(producto_venta.precio_venta)
            total_pedido += precio_unitario * total_unidades

            detalles.append(
                {
                    "producto_venta_id": producto_venta_id,
                    "receta_id": receta.id,
                    "cantidad": cantidad,
                    "cantidad_lotes": cantidad_lotes,
                    "total_unidades": total_unidades,
                    "precio_unitario": precio_unitario,
                    "receta": receta,
                }
            )

            for ingrediente in receta.detalle:
                cantidad_insumo = ingrediente.cantidad * cantidad_lotes * 1.1
                solicitudes_agrupadas[ingrediente.materia_prima_id] = (
                    solicitudes_agrupadas.get(ingrediente.materia_prima_id, 0.0)
                    + cantidad_insumo
                )

        try:
            pedido = pedido_repo.create_pedido(
                cliente_id,
                detalles,
                total_pedido,
                current_user.id if current_user.is_authenticated else None,
            )

            solicitud_ids = []
            for materia_prima_id, cantidad in solicitudes_agrupadas.items():
                solicitud = create_solicitud(
                    materia_prima_id=materia_prima_id,
                    cantidad=round(cantidad, 4),
                    origen="retail",
                    referencia_id=pedido.id,
                )
                solicitud_ids.append(solicitud.id)

            produccion_service = ProduccionService()
            primer_solicitud_id = solicitud_ids[0] if solicitud_ids else None
            for detalle in detalles:
                produccion = produccion_service.crear_produccion(
                    {
                        "id_receta": detalle["receta_id"],
                        "cantidad": detalle["cantidad_lotes"],
                        "es_retail": True,
                        "id_solicitud_compra": primer_solicitud_id,
                    },
                    commit=False,
                )
                pedido_repo.create_pedido_produccion(
                    pedido.id, produccion.id_produccion
                )

            db.session.commit()
            return pedido
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error interno al crear el pedido: {str(e)}")

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

        pedido.usuario_id = (
            current_user.id if current_user.is_authenticated else pedido.usuario_id
        )
        pedido_repo.update_pedido_estado(
            pedido,
            "Cancelado",
            current_user.id if current_user.is_authenticated else None,
        )
        return pedido
