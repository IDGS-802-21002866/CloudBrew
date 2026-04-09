from app.modules.inventario_materias_primas.service import InventarioMateriasPrimasService
from app.modules.produccion.repository import (
    eliminar_produccion_proceso,
    get_procesos_por_produccion,
    get_produccion,
    get_produccion_by_id,
    insertar_produccion,
    insertar_produccion_proceso,
    eliminar_produccion,
    modificar_produccion,
    eliminar_produccion,
    modificar_produccion_proceso)
from .forms import ProduccionForm
from app.modules.produccion.forms import ProduccionProcesoForm
from app.modules.recetas.service import RecetaService
RecetaService=RecetaService()
class ProduccionService:

    def crear_produccion(self, form: ProduccionForm):
        try:

            receta = RecetaService.obtener_receta(form.id_receta.data)
            if not receta:
                raise ValueError("Receta no encontrada")
            stock_materias = InventarioMateriasPrimasService().listar_materias_primas_con_stock()
            stock_dict = {m["id"]: m["stock_actual"] for m in stock_materias}

            for detalle in receta.detalle:
                materia_id = detalle.materia_prima_id
                cantidad_necesaria = detalle.cantidad * form.cantidad.data

                stock_disponible = stock_dict.get(materia_id, 0)

                if stock_disponible < cantidad_necesaria:
    
                    raise ValueError(
                        f"Stock insuficiente para la materia prima ID {materia_id}. "
                        f"Necesario: {cantidad_necesaria}, Disponible: {stock_disponible}"
                    )
                
            produccion = insertar_produccion(form)

            if isinstance(produccion, ValueError):
                raise produccion

            for proceso_receta in receta.procesos_receta:
                proceso_form = ProduccionProcesoForm()
                proceso_form.id_proceso.data = proceso_receta.proceso_productivo_id
                proceso_form.fecha_inicio.data = form.fecha_inicio.data
                proceso_form.fecha_fin.data = form.fecha_fin.data
                proceso_form.estado.data = "pendiente"

                proceso = insertar_produccion_proceso(
                    produccion.id_produccion,
                    proceso_form
                )
                if isinstance(proceso, ValueError):
                    eliminar_produccion(produccion.id_produccion)
                    raise proceso

            return produccion

        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Error interno al crear producción: {str(e)}")
    
    def actualizar_produccion(self, id_produccion, form: ProduccionForm):
            try:

                receta = RecetaService.obtener_receta(form.id_receta.data)
                if not receta:
                    raise ValueError("Receta no encontrada")

                stock_materias = InventarioMateriasPrimasService().listar_materias_primas_con_stock()
                stock_dict = {m["id"]: m["stock_actual"] for m in stock_materias}

                for detalle in receta.detalle:
                    materia_id = detalle.materia_prima_id
                    cantidad_necesaria = detalle.cantidad * form.cantidad.data

                    stock_disponible = stock_dict.get(materia_id, 0)

                    if stock_disponible < cantidad_necesaria:
                        raise ValueError(
                            f"Stock insuficiente para la materia prima ID {materia_id}. "
                            f"Necesario: {cantidad_necesaria}, Disponible: {stock_disponible}"
                        )

                produccion = modificar_produccion(id_produccion, form)
                
                if isinstance(produccion, ValueError):
                    raise produccion

                procesos_query = get_procesos_por_produccion(id_produccion)
                
                if not isinstance(procesos_query, ValueError):
                    procesos_actuales = procesos_query.all()
                    
                    for proceso_actual in procesos_actuales:
                        proceso_form = ProduccionProcesoForm()
                        
                        proceso_form.id_proceso.data = proceso_actual.id_proceso
                        proceso_form.fecha_inicio.data = form.fecha_inicio.data
                        proceso_form.fecha_fin.data = form.fecha_fin.data
                        proceso_form.estado.data = proceso_actual.estado

                        proceso_modificado = modificar_produccion_proceso(
                            proceso_actual.id_produccion_proceso, 
                            proceso_form
                        )
                        
                        if isinstance(proceso_modificado, ValueError):
                            raise proceso_modificado

                return produccion

            except ValueError as e:
                raise e
            except Exception as e:
                raise ValueError(f"Error interno al modificar producción: {str(e)}")
            
    def cancelar_produccion(self, id_produccion):
        try:
            produccion_cancelada = eliminar_produccion(id_produccion)
            
            if isinstance(produccion_cancelada, ValueError):
                raise produccion_cancelada

        
            procesos_query = get_procesos_por_produccion(id_produccion)
            
            if not isinstance(procesos_query, ValueError):
                procesos_actuales = procesos_query.all()
                
                for proceso_actual in procesos_actuales:
                    proceso_cancelado = eliminar_produccion_proceso(
                        proceso_actual.id_produccion_proceso
                    )
                    
                    if isinstance(proceso_cancelado, ValueError):
                        raise proceso_cancelado

            return produccion_cancelada

        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Error interno al intentar cancelar la producción: {str(e)}")

    def obtener_procesos_de_produccion(self, id_produccion):
            return get_procesos_por_produccion(id_produccion)

    def listar_toda_la_produccion(self):
            return get_produccion()

    def buscar_produccion_por_id(self, id):
            return get_produccion_by_id(id)