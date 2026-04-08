from app.modules.inventario_producto_terminado import repository


class InventarioProductoTerminadoService:
    def listar_recetas_con_stock(self):
        inventario = repository.get_all_recetas_con_stock()
        resultado = []

        for item in inventario:
            stock_actual = float(item.stock_actual or 0)

            resultado.append(
                {
                    "id": item.id,
                    "nombre": item.nombre,
                    "descripcion": item.descripcion,
                    "cantidad_producida": item.cantidad_producida,
                    "stock_actual": stock_actual,
                    "estado_stock": self._obtener_estado_stock(stock_actual),
                }
            )

        return resultado

    def _obtener_estado_stock(self, stock_actual):
        if stock_actual <= 0:
            return "sin_stock"
        return "disponible"

    def obtener_receta(self, receta_id):
        receta = repository.get_receta_by_id(receta_id)
        if not receta:
            raise ValueError("Receta no encontrada.")
        return receta

    def listar_movimientos_receta(self, receta_id):
        self.obtener_receta(receta_id)
        return repository.get_all_movimientos_by_receta_id(receta_id)

    def obtener_stock_actual_receta(self, receta_id):
        self.obtener_receta(receta_id)
        return repository.get_stock_actual_by_receta_id(receta_id)
