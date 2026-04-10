from app import db
from sqlalchemy import func
from app.modules.inventario_producto_terminado.model import MovimientosReceta
from app.modules.mermas_producto_terminado import repository as merma_repo
from app.modules.mermas_producto_terminado.model import MermaProductoTerminado


class MermaProductoTerminadoService:
    def listar_paginados(self, page=1, per_page=10, search_term=None):
        return merma_repo.get_paginated_mermas(page, per_page, search_term)

    def obtener_merma_por_id(self, merma_id):
        merma = merma_repo.get_merma_by_id(merma_id)
        if not merma:
            raise ValueError("Merma no encontrada.")
        return merma

    def obtener_stock_actual(self, receta_id):
        entradas = db.session.query(func.sum(MovimientosReceta.cantidad))
        entradas = entradas.filter(
            MovimientosReceta.receta_id == receta_id,
            MovimientosReceta.tipo == "entrada",
        ).scalar() or 0

        salidas = db.session.query(func.sum(MovimientosReceta.cantidad))
        salidas = salidas.filter(
            MovimientosReceta.receta_id == receta_id,
            MovimientosReceta.tipo == "salida",
        ).scalar() or 0

        return entradas - salidas

    def registrar_merma(self, data, usuario_id):
        r_id = data.get("receta_id")
        if not r_id: raise ValueError("Selecciona un producto de la lista.")
        
        cantidad = float(data.get("cantidad") or 0)
        l_id = int(data.get("lote_id")) if data.get("lote_id") else None
        es_completo = data.get("es_lote_completo")

        # 1. Crear registro de merma
        nueva_merma = MermaProductoTerminado(
            receta_id=int(r_id), lote_id=l_id, cantidad=cantidad,
            motivo=data.get("motivo"), usuario_id=usuario_id
        )
        db.session.add(nueva_merma)

        # 2. SI ES LOTE COMPLETO, INACTIVARLO
        if es_completo and l_id:
            from app.modules.lotes.model import LoteProduccion 
            lote_obj = db.session.get(LoteProduccion, l_id)
            if lote_obj:
                lote_obj.activo = False # Manuel usa este campo para "borrar" lógicamente

        # 3. Movimiento de Inventario
        mov = MovimientosReceta(
            receta_id=int(r_id), tipo="salida", cantidad=cantidad,
            motivo=f"Merma: {data.get('motivo')}", usuario_id=usuario_id
        )
        db.session.add(mov)
        db.session.commit()
        return nueva_merma