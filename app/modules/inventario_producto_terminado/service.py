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

    def listar_recetas_con_stock_pag(self, page, per_page):
        paginated = repository.get_paginated_recetas_con_stock(page, per_page)

        resultado = []

        for item in paginated.items:
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
        paginated.items = resultado

        return paginated

    def _obtener_estado_stock(self, stock_actual):
        if stock_actual <= 0:
            return "sin_stock"
        return "disponible"

    def listar_recetas_bajo_stock_pag(self, page=1, per_page=10):
        paginated = repository.get_paginated_recetas_con_stock(page=1, per_page=1000)

        resultado = []
        for item in paginated.items:
            stock_actual = float(item.stock_actual or 0)
            if stock_actual <= 0:
                resultado.append(
                    {
                        "id": item.id,
                        "nombre": item.nombre,
                        "descripcion": item.descripcion,
                        "cantidad_producida": item.cantidad_producida,
                        "stock_actual": stock_actual,
                        "estado_stock": "sin_stock",
                    }
                )

        # Manual pagination
        total = len(resultado)
        start = (page - 1) * per_page
        end = start + per_page
        pagina_items = resultado[start:end]

        from flask_sqlalchemy.pagination import Pagination

        class PaginacionManual:
            def __init__(self, items, page, per_page, total):
                self.items = items
                self.page = page
                self.per_page = per_page
                self.total = total
                self.pages = max(1, (total + per_page - 1) // per_page)
                self.has_prev = page > 1
                self.has_next = page < self.pages
                self.prev_num = page - 1 if self.has_prev else None
                self.next_num = page + 1 if self.has_next else None

        return PaginacionManual(pagina_items, page, per_page, total)

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
