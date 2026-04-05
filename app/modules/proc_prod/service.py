from app.modules.proc_prod.repository import (
    obtener_por_id,
    obtener_paginados,
    insertar,
    modificar,
    eliminacion_logica
)

class ProcesoProductivoService:
    @staticmethod
    def obtener_proc_por_id(proceso_id: int):
        return obtener_por_id(proceso_id)
    
    @staticmethod
    def obtener_procesos(pag, querry=""):
        if querry:
            filtrados = [
                proceso for proceso in pag.items
                if querry.lower() in (proceso.nombre or "").lower()
            ]
            pag.items = filtrados

        return pag

    @staticmethod
    def obtener_procesos(page: int = 1, per_page: int = 5,querry: str = ""):
        return obtener_paginados(page, per_page)

    @staticmethod
    def insertar_proc(form):
        return insertar(form)

    @staticmethod
    def modificar_proc(proceso_id: int, form):
        return modificar(proceso_id, form)

    @staticmethod
    def eliminar_proc(proceso_id: int):
        return eliminacion_logica(proceso_id)