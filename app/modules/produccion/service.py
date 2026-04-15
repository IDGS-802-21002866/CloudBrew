from flask_login import current_user
from app import db
from app.modules.inventario_materias_primas.service import (
    InventarioMateriasPrimasService,
)
from app.modules.inventario_materias_primas.model import MovimientosMateriaPrima
from app.modules.produccion.repository import (
    eliminar_produccion_proceso,
    get_pedido_produccion_por_produccion,
    get_procesos_por_produccion,
    get_produccion,
    get_produccion_by_id,
    insertar_produccion,
    insertar_produccion_proceso,
    eliminar_produccion,
    modificar_produccion,
    modificar_produccion_proceso,
)
from .forms import ProduccionForm
from app.modules.recetas.service import RecetaService

receta_service = RecetaService()
inventario_service = InventarioMateriasPrimasService()

RecetaService=RecetaService()
class ProduccionService:

    def listar_produccion(self):
        return get_produccion()

    def crear_produccion(self, data: dict, commit=True):
        from app import db

        id_receta = data.get("id_receta")
        cantidad = data.get("cantidad")

        if not id_receta:
            raise ValueError("Debe seleccionar una receta.")
        if not cantidad or int(cantidad) < 1:
            raise ValueError("La cantidad debe ser mayor a cero.")

        receta = receta_service.obtener_receta(id_receta)
        if not receta:
            raise ValueError("Receta no encontrada.")
        if not receta.procesos_receta:
            raise ValueError("La receta no tiene procesos asociados.")

        es_retail = bool(data.get("es_retail"))
        solicitud_compra_id = data.get("id_solicitud_compra")

        if not es_retail:
            for detalle in receta.detalle:
                cantidad_necesaria = detalle.cantidad * int(cantidad)
                stock_disponible = inventario_service.obtener_stock_actual_materia_prima(
                    detalle.materia_prima_id
                )
                if stock_disponible < cantidad_necesaria:
                    raise ValueError(
                        f"Stock insuficiente para la materia prima '{detalle.materia_prima.nombre}'. "
                        f"Necesario: {cantidad_necesaria}, Disponible: {stock_disponible}"
                    )

        try:
            produccion = insertar_produccion(
                id_receta,
                int(cantidad),
                current_user.id if current_user.is_authenticated else None,
                es_retail=es_retail,
                id_solicitud_compra=solicitud_compra_id,
            )

            for proceso_receta in receta.procesos_receta:
                insertar_produccion_proceso(
                    produccion.id_produccion,
                    proceso_receta.proceso_productivo_id,
                    proceso_receta.orden,
                    proceso_receta.tiempo_estimado,
                )

            if es_retail:
                self._registrar_movimientos_virtuales(produccion, receta)

            if commit and not db.session.in_transaction():
                db.session.commit()
            return produccion

        except Exception as e:
            if not db.session.in_transaction():
                db.session.rollback()
            raise ValueError(f"Error interno al crear producción: {str(e)}")

    def _registrar_movimientos_virtuales(self, produccion, receta):
        cantidades_por_mp = {}
        for detalle in receta.detalle:
            cantidad_necesaria = detalle.cantidad * produccion.cantidad
            cantidades_por_mp[detalle.materia_prima_id] = (
                cantidades_por_mp.get(detalle.materia_prima_id, 0) + cantidad_necesaria
            )

        for materia_prima_id, cantidad in cantidades_por_mp.items():
            for tipo, motivo in [
                ("entrada", "Entrada Virtual"),
                ("salida", "Salida Virtual"),
            ]:
                movimiento = MovimientosMateriaPrima(
                    materia_prima_id=materia_prima_id,
                    tipo=tipo,
                    cantidad=cantidad,
                    motivo=motivo,
                    usuario_id=current_user.id if current_user.is_authenticated else None,
                    produccion_id=produccion.id_produccion,
                )
                db.session.add(movimiento)

    def _registrar_buffer_finalizacion(self, produccion, receta):
        for detalle in receta.detalle:
            cantidad_necesaria = detalle.cantidad * produccion.cantidad
            buffer = round(cantidad_necesaria * 0.10, 4)
            if buffer <= 0:
                continue
            movimiento = MovimientosMateriaPrima(
                materia_prima_id=detalle.materia_prima_id,
                tipo="entrada",
                cantidad=buffer,
                motivo="Buffer Retail no utilizado",
                usuario_id=current_user.id if current_user.is_authenticated else None,
                produccion_id=produccion.id_produccion,
            )
            db.session.add(movimiento)

    def actualizar_produccion(self, id_produccion, form: ProduccionForm):
        try:
            receta = receta_service.obtener_receta(form.id_receta.data)
            if not receta:
                raise ValueError("Receta no encontrada")

            produccion_actual = get_produccion_by_id(id_produccion)
            if not produccion_actual:
                raise ValueError("Producción no encontrada.")

            if not produccion_actual.es_retail:
                for detalle in receta.detalle:
                    cantidad_necesaria = detalle.cantidad * form.cantidad.data
                    stock_disponible = (
                        inventario_service.obtener_stock_actual_materia_prima(
                            detalle.materia_prima_id
                        )
                    )

                    if stock_disponible < cantidad_necesaria:
                        raise ValueError(
                            f"Stock insuficiente para la materia prima ID {detalle.materia_prima_id}. "
                            f"Necesario: {cantidad_necesaria}, Disponible: {stock_disponible}"
                        )

            estado_anterior = produccion_actual.estado
            produccion = modificar_produccion(
                id_produccion,
                form.id_receta.data,
                form.cantidad.data,
                form.estado.data,
                current_user.id if current_user.is_authenticated else None,
            )

            if isinstance(produccion, ValueError):
                raise produccion

            if (
                produccion_actual.es_retail
                and estado_anterior != "Terminado"
                and form.estado.data == "Terminado"
            ):
                receta_final = receta_service.obtener_receta(produccion_actual.id_receta)
                if receta_final:
                    self._registrar_buffer_finalizacion(produccion, receta_final)
                    if not db.session.in_transaction():
                        db.session.commit()

            procesos_query = get_procesos_por_produccion(id_produccion)

            if not isinstance(procesos_query, ValueError):
                for proceso_actual in procesos_query.all():
                    resultado = modificar_produccion_proceso(
                        proceso_actual.id_produccion_proceso,
                        proceso_actual.id_proceso,
                        proceso_actual.estado,
                    )
                    if isinstance(resultado, ValueError):
                        raise resultado

            return produccion

        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Error interno al modificar producción: {str(e)}")

    def cancelar_produccion(self, id_produccion):
        vinculo = get_pedido_produccion_por_produccion(id_produccion)
        if vinculo:
            raise ValueError(
                "No se puede cancelar una producción vinculada a un pedido. "
                "Cancele el pedido directamente."
            )
        return self.cancelar_produccion_forzada(id_produccion)

    def cancelar_produccion_forzada(self, id_produccion):
        try:
            produccion_cancelada = eliminar_produccion(
                id_produccion,
                current_user.id if current_user.is_authenticated else None,
            )

            if isinstance(produccion_cancelada, ValueError):
                raise produccion_cancelada

            procesos = get_procesos_por_produccion(id_produccion)

            if not isinstance(procesos, ValueError):
                for proceso in procesos:
                    resultado = eliminar_produccion_proceso(
                        proceso.id_produccion_proceso
                    )
                    if isinstance(resultado, ValueError):
                        raise resultado

            return produccion_cancelada

        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(
                f"Error interno al intentar cancelar la producción: {str(e)}"
            )

    def obtener_procesos_de_produccion(self, id_produccion):
        return get_procesos_por_produccion(id_produccion)

    def listar_toda_la_produccion(self):
        return get_produccion()

    def buscar_produccion_por_id(self, id):
        return get_produccion_by_id(id)
