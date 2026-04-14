from app.modules.costos import repository


class CostoService:

    def calcular_costo_materia_prima(self, materia_prima_id):
        """Retorna el costo promedio por unidad base de una materia prima."""
        return repository.get_costo_promedio_materia_prima(materia_prima_id)

    def calcular_costo_receta(self, receta):
        """
        Calcula el costo de produccion de un batch completo de una receta
        y el costo unitario por unidad producida.

        Returns:
            dict con costo_total, costo_unitario, ingredientes, advertencias
        """
        costo_total = 0.0
        advertencias = []
        ingredientes = []

        for detalle in receta.detalle:
            costo_mp = self.calcular_costo_materia_prima(detalle.materia_prima_id)
            if costo_mp == 0:
                advertencias.append(detalle.materia_prima.nombre)
            costo_ingrediente = costo_mp * detalle.cantidad
            costo_total += costo_ingrediente
            ingredientes.append(
                {
                    "nombre": detalle.materia_prima.nombre,
                    "cantidad": detalle.cantidad,
                    "costo_promedio": costo_mp,
                    "subtotal": costo_ingrediente,
                }
            )

        cantidad_producida = receta.cantidad_producida or 1
        costo_unitario = costo_total / cantidad_producida

        return {
            "costo_total": costo_total,
            "costo_unitario": costo_unitario,
            "ingredientes": ingredientes,
            "advertencias": advertencias,
        }

    def listar_dashboard(self):
        """Retorna datos de costos de todas las recetas y materias primas activas."""
        recetas = repository.get_all_recetas_activas()
        materias_primas = repository.get_all_materias_primas_activas()

        recetas_data = []
        for receta in recetas:
            costo_info = self.calcular_costo_receta(receta)
            recetas_data.append(
                {
                    "id": receta.id,
                    "nombre": receta.nombre,
                    "cantidad_producida": receta.cantidad_producida,
                    "costo_unitario": costo_info["costo_unitario"],
                    "tiene_advertencias": bool(costo_info["advertencias"]),
                }
            )

        mps_data = []
        for mp in materias_primas:
            costo = self.calcular_costo_materia_prima(mp.id)
            mps_data.append(
                {
                    "id": mp.id,
                    "nombre": mp.nombre,
                    "costo_promedio": costo,
                    "sin_datos": costo == 0,
                }
            )

        return {
            "recetas": recetas_data,
            "materias_primas": mps_data,
        }

    def obtener_detalle_costo_receta(self, receta_id):
        """Retorna el desglose completo de costo de una receta."""
        from app.modules.recetas.repository import get_receta_by_id

        receta = get_receta_by_id(receta_id)
        if not receta:
            raise ValueError("Receta no encontrada.")
        return self.calcular_costo_receta(receta)
