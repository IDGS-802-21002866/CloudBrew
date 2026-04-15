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

        # Si no se especificó un lote, usar FIFO para encontrar lotes disponibles
        if not l_id:
            lotes_disponibles = self.obtener_lotes_disponibles_por_receta(r_id)
            if not lotes_disponibles:
                raise ValueError('No hay lotes disponibles con stock para este producto.')
            
            # Registrar merma usando FIFO (puede afectar múltiples lotes)
            return self.registrar_merma_multilotes(
                receta_id=r_id,
                cantidad_total=cantidad,
                motivo=motivo,
                usuario_id=usuario_id,
                lotes_disponibles=lotes_disponibles
            )
        
        # Si se especificó un lote, validarlo
        from app.modules.lotes.model import LoteProduccion
        lote_obj = db.session.get(LoteProduccion, l_id)
        if not lote_obj:
            raise ValueError('El lote seleccionado no existe.')
        
        # Verificar disponibilidad específica del lote
        stock_lote = self.obtener_stock_lote(l_id)
        if cantidad > stock_lote:
            raise ValueError(
                f'El lote {lote_obj.codigo_lote} solo tiene {stock_lote} unidades disponibles. '
                f'No puedes mermar {cantidad}.'
            )
        
        if es_completo:
            cantidad = float(stock_lote)  # Mermar todo el lote
        
        if cantidad <= 0:
            raise ValueError('La cantidad de merma debe ser mayor a cero.')
        
        try:
            # Registrar merma para un lote específico
            return self._registrar_merma_lote_unico(
                receta_id=r_id,
                lote_id=l_id,
                lote_obj=lote_obj,
                cantidad=cantidad,
                motivo=motivo,
                usuario_id=usuario_id,
                es_completo=es_completo
            )
        except Exception:
            db.session.rollback()
            raise
    
    def obtener_stock_lote(self, lote_id):
        """Obtiene el stock actual de un lote específico"""
        from app.modules.movimientos_receta.model import MovimientosReceta
        
        # Obtener el lote
        lote = db.session.get(LoteProduccion, lote_id)
        if not lote:
            return 0
        
        # Calcular salidas de este lote
        total_salidas = db.session.query(db.func.sum(MovimientosReceta.cantidad))\
            .filter(
                MovimientosReceta.lote_id == lote_id,
                MovimientosReceta.tipo == 'salida'
            ).scalar() or 0
        
        # La cantidad_generada es la producción inicial del lote
        stock_disponible = lote.cantidad_generada - total_salidas
        
        return max(0, stock_disponible)

    def obtener_lotes_disponibles_por_receta(self, receta_id):
        """Obtiene todos los lotes con stock disponible para una receta"""
        from app.modules.lotes.model import LoteProduccion
        from app.modules.produccion.model import Produccion
        
        # Subconsulta para obtener producciones de esta receta
        producciones = db.session.query(Produccion.id_produccion)\
            .filter(Produccion.id_receta == receta_id)\
            .subquery()
        
        # Obtener lotes de esas producciones que aún tienen stock
        lotes = db.session.query(LoteProduccion).filter(
            LoteProduccion.id_produccion.in_(producciones)
        ).all()
        
        # Filtrar solo lotes con stock disponible
        lotes_con_stock = []
        for lote in lotes:
            stock = self.obtener_stock_lote(lote.id_lote)
            if stock > 0:
                lote.stock_actual = stock  # Agregar atributo temporal
                lotes_con_stock.append(lote)
        
        return lotes_con_stock