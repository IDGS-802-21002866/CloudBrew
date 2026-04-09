from app.modules.proc_prod.repository import (
    get_proceso_productivo_by_id,
    get_all_procesos_productivos,
    create_proceso_productivo,
    update_proceso_productivo,
    delete_proceso_productivo,
)


class ProcesoProductivoService:
    def obtener_por_id(self, proceso_id: int):
        return get_proceso_productivo_by_id(proceso_id)

    def listar_procesos(self, page: int = 1, per_page: int = 5, querry: str = ""):
        pag = get_all_procesos_productivos(page, per_page)
        if querry:
            filtrados = [
                proceso
                for proceso in pag.items
                if querry.lower() in (proceso.nombre or "").lower()
            ]
            pag.items = filtrados
        return pag

    def crear_proceso(self, form):
        return create_proceso_productivo(form)

    def actualizar_proceso(self, proceso_id: int, form):
        return update_proceso_productivo(proceso_id, form)

    def eliminar_proceso(self, proceso_id: int):
        return delete_proceso_productivo(proceso_id)
