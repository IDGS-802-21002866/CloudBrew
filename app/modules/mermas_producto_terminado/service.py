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
        entradas = db.session.query(func.sum(MovimientosReceta.cantidad)).filter(
            MovimientosReceta.receta_id == receta_id,
            MovimientosReceta.tipo == 'entrada'
        ).scalar() or 0
        
        salidas = db.session.query(func.sum(MovimientosReceta.cantidad)).filter(
            MovimientosReceta.receta_id == receta_id,
            MovimientosReceta.tipo == 'salida'
        ).scalar() or 0
        
        return entradas - salidas

    def registrar_merma(self, data, usuario_id):
        r_id = data.get('receta_id')
        motivo = (data.get('motivo') or '').strip()
        cantidad = float(data.get('cantidad') or 0)
        l_id = int(data.get('lote_id')) if data.get('lote_id') else None
        es_completo = data.get('es_lote_completo')

        if not r_id:
            raise ValueError('Debes seleccionar un producto de la lista.')
        if len(motivo) < 10:
            raise ValueError('El motivo debe tener al menos 10 caracteres.')
        if len(motivo) > 255:
            raise ValueError('El motivo no puede tener más de 255 caracteres.')
        if cantidad <= 0:
            raise ValueError('La cantidad de merma debe ser mayor a cero.')

        lote_obj = None
        if l_id:
            from app.modules.lotes.model import LoteProduccion

            lote_obj = db.session.get(LoteProduccion, l_id)
            if not lote_obj:
                raise ValueError('El lote seleccionado no existe.')
            if es_completo:
                cantidad = float(getattr(lote_obj, 'cantidad_generada', cantidad) or cantidad)
            if cantidad <= 0:
                raise ValueError('La cantidad de merma debe ser mayor a cero.')

        stock_actual = self.obtener_stock_actual(int(r_id))
        if cantidad > stock_actual:
            raise ValueError(
                f'No puedes mermar más de lo que hay en existencia (Máx: {stock_actual})'
            )

        try:
            nueva_merma = MermaProductoTerminado(
                receta_id=int(r_id),
                lote_id=l_id,
                cantidad=cantidad,
                motivo=motivo,
                usuario_id=usuario_id,
                activo=True,
            )
            db.session.add(nueva_merma)
            db.session.flush()

            if es_completo and lote_obj and hasattr(lote_obj, 'activo'):
                lote_obj.activo = False

            mov = MovimientosReceta(
                receta_id=int(r_id),
                lote_id=l_id,
                tipo='salida',
                cantidad=cantidad,
                motivo=f'Merma {nueva_merma.folio}: {motivo}',
                usuario_id=usuario_id,
            )
            db.session.add(mov)

            db.session.commit()
            return nueva_merma
        except Exception:
            db.session.rollback()
            raise
