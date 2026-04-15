from app.modules.lotes.repository import (
    insertar_lote_produccion,
    eliminar_lote_produccion,
    obtener_lote_produccion,
    obtener_lotes_por_produccion,
    obtener_lotes_por_receta,
    listar_lotes_con_paginacion,
)

class LoteProduccionService:

    def insertar(self,form):
        return insertar_lote_produccion(form)

    def eliminar(self,id_lote):
        return eliminar_lote_produccion(id_lote)

    def obtener(self,id_lote):
        return obtener_lote_produccion(id_lote)

    def obtener_por_produccion(self,id_produccion):
        return obtener_lotes_por_produccion(id_produccion)

    def obtener_por_receta(self, receta_id):
        return obtener_lotes_por_receta(receta_id)

    def obtener_lotes_paginados(self, page=1, per_page=10, querry=""):
        return listar_lotes_con_paginacion(page=page, per_page=per_page, querry=querry)