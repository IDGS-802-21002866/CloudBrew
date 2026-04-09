from app.modules.inventario_materias_primas.service import (
    InventarioMateriasPrimasService,
)
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

    def crear_produccion(self, data: dict):
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
            produccion = insertar_produccion(id_receta, int(cantidad))

            for proceso_receta in receta.procesos_receta:
                insertar_produccion_proceso(
                    produccion.id_produccion,
                    proceso_receta.proceso_productivo_id,
                    proceso_receta.orden,
                    proceso_receta.tiempo_estimado,
                )

            db.session.commit()
            return produccion

        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error interno al crear producción: {str(e)}")

    def actualizar_produccion(self, id_produccion, form: ProduccionForm):
        try:
            receta = receta_service.obtener_receta(form.id_receta.data)
            if not receta:
                raise ValueError("Receta no encontrada")

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

            produccion = modificar_produccion(
                id_produccion, form.id_receta.data, form.cantidad.data, form.estado.data
            )

            if isinstance(produccion, ValueError):
                raise produccion

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
            produccion_cancelada = eliminar_produccion(id_produccion)

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
