from app.modules.inventario_materias_primas import repository


class InventarioMateriasPrimasService:
    def listar_materias_primas_con_stock(self):
        inventario = repository.get_all_materias_primas_con_stock()
        resultado = []

        for item in inventario:
            stock_actual = float(item.stock_actual or 0)
            stock_minimo = float(item.stock_minimo or 0)

            resultado.append(
                {
                    "id": item.id,
                    "nombre": item.nombre,
                    "tipo_medida_id": item.tipo_medida_id,
                    "stock_minimo": stock_minimo,
                    "stock_actual": stock_actual,
                    "estado_stock": self._obtener_estado_stock(
                        stock_actual, stock_minimo
                    ),
                }
            )

        return resultado

    def _obtener_estado_stock(self, stock_actual, stock_minimo):
        if stock_actual == 0:
            return "sin_stock"
        if stock_actual < stock_minimo:
            return "bajo_stock"
        return "disponible"

    def obtener_materia_prima(self, materia_prima_id):
        materia_prima = repository.get_materia_prima_by_id(materia_prima_id)
        if not materia_prima:
            raise ValueError("Materia prima no encontrada.")
        return materia_prima

    def listar_movimientos_materia_prima(self, materia_prima_id):
        self.obtener_materia_prima(materia_prima_id)
        return repository.get_all_movimientos_by_materia_prima_id(materia_prima_id)

    def obtener_stock_actual_materia_prima(self, materia_prima_id):
        self.obtener_materia_prima(materia_prima_id)
        return repository.get_stock_actual_by_materia_prima_id(materia_prima_id)
