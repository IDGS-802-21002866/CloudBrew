from app import db
from app.modules.inventario_materias_primas import repository as inv_repo
from app.modules.mermas_materia_prima import repository as merma_repo
from app.modules.mermas_materia_prima.model import MermaMateriaPrima
from app.modules.inventario_materias_primas.model import MovimientosMateriaPrima
from sqlalchemy import func
from flask_login import current_user


class MermaMateriaPrimaService:
    def listar_paginados(self, page=1, per_page=10, search_term=None):
        return merma_repo.get_paginated_mermas(page, per_page, search_term)

    def obtener_merma_por_id(self, merma_id):
        merma = merma_repo.get_merma_by_id(merma_id)
        if not merma:
            raise ValueError("Merma no encontrada.")
        return merma

    def obtener_stock_actual(self, mp_id):
        # Stock = Σ(entradas) - Σ(salidas)
        entradas = db.session.query(func.sum(MovimientosMateriaPrima.cantidad)).filter(
            MovimientosMateriaPrima.materia_prima_id == mp_id,
            MovimientosMateriaPrima.tipo == 'entrada'
        ).scalar() or 0
        
        salidas = db.session.query(func.sum(MovimientosMateriaPrima.cantidad)).filter(
            MovimientosMateriaPrima.materia_prima_id == mp_id,
            MovimientosMateriaPrima.tipo == 'salida'
        ).scalar() or 0
        
        return entradas - salidas

    def registrar_merma(self, data, usuario_id):
        mp_id = data.get('materia_prima_id')
        cantidad = float(data.get('cantidad'))
        
        # VALIDACIÓN: No mermar más de lo que hay
        stock_disp = self.obtener_stock_actual(mp_id)
        if cantidad > stock_disp:
            raise ValueError(f"No hay suficiente stock. Disponible: {stock_disp}")

        try:
            # El movimiento de salida se crea manualmente aquí. No contamos con el trigger SQL
            # activo para evitar doble descuento de stock.
            nueva_merma = MermaMateriaPrima(
                materia_prima_id=mp_id,
                cantidad=cantidad,
                motivo=data.get('motivo'),
                usuario_id=usuario_id
            )
            db.session.add(nueva_merma)
            db.session.flush()  # Para obtener el ID de la merma

            mov = MovimientosMateriaPrima(
                materia_prima_id=mp_id,
                tipo='salida',
                cantidad=cantidad,
                motivo=f"Merma Folio: {nueva_merma.id} - {data.get('motivo')}",
                usuario_id=usuario_id,
                merma_materia_prima_id=nueva_merma.id
            )
            db.session.add(mov)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def cancelar(self, merma_id):
        merma = merma_repo.get_merma_by_id(merma_id)
        if not merma or not merma.activo:
            raise ValueError("Merma no encontrada o ya está cancelada.")

        merma.usuario_id = current_user.id if current_user.is_authenticated else merma.usuario_id
        return merma_repo.deactivate(merma)
