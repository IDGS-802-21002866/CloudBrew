from app.modules.inventario_materias_primas import repository as inv_repo
from app.modules.mermas_materia_prima import repository as merma_repo
from app.modules.mermas_materia_prima.model import MermaMateriaPrima
from flask_login import current_user


class MermaMateriaPrimaService:
    def listar_paginados(self, page=1, per_page=10, search_term=None):
        return merma_repo.get_paginated_mermas(page, per_page, search_term)

    def obtener_merma_por_id(self, merma_id):
        merma = merma_repo.get_merma_by_id(merma_id)
        if not merma:
            raise ValueError("Merma no encontrada.")
        return merma

    def registrar_merma(self, data, usuario_id=None):
        if usuario_id is None:
            usuario_id = current_user.id if current_user.is_authenticated else None
            
        mp_id = data.get("materia_prima_id")
        if not mp_id:
            raise ValueError("Debe seleccionar una materia prima.")

        try:
            cantidad = float(data.get("cantidad"))
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número válido.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        stock_actual = inv_repo.get_stock_actual_by_materia_prima_id(mp_id)
        if stock_actual < cantidad:
            raise ValueError(
                f"No hay stock suficiente. Disponible: {stock_actual:.2f}"
            )

        motivo = data.get("motivo", "").strip()
        if not motivo:
            raise ValueError("El motivo es obligatorio.")

        nueva_merma = MermaMateriaPrima(
            materia_prima_id=mp_id,
            cantidad=cantidad,
            motivo=motivo,
            usuario_id=usuario_id,
        )
        return merma_repo.save(nueva_merma)

    def cancelar(self, merma_id):
        merma = merma_repo.get_merma_by_id(merma_id)
        if not merma or not merma.activo:
            raise ValueError("Merma no encontrada o ya está cancelada.")

        merma.usuario_id = current_user.id if current_user.is_authenticated else merma.usuario_id
        return merma_repo.deactivate(merma)
