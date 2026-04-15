from app.modules.inventario_materias_primas import repository

class InventarioMateriasPrimasService:
    def listar_materias_primas_paginadas(self, page=1, per_page=10, search_term=None):
        pagination = repository.get_all_materias_primas_con_stock(page, per_page, search_term)
        
        todo_el_inventario = repository.get_all_materias_primas_con_stock(page=1, per_page=1000, search_term=search_term).items
        
        bajo_stock_total = 0
        sin_stock_total = 0

        for item in todo_el_inventario:
            stock_min_base = float(item.max_receta or 0) * 2
            stock_act_base = float(item.stock_actual_base or 0)
            estado = self._obtener_estado_stock(stock_act_base, stock_min_base)
            if estado == "sin_stock": sin_stock_total += 1
            elif estado == "bajo_stock": bajo_stock_total += 1

        items_procesados = []
        for item in pagination.items:
            item_dict = dict(item._asdict())
            factor = float(item_dict.get('valor_conversion') or 1)
            
            abr = item_dict.get('unidad_abreviatura')
            if not abr:
                tipo = item_dict.get('tipo_medida_id')
                if tipo == 1: abr = "g"
                elif tipo == 2: abr = "ml"
                else: abr = "pzas"

            stock_min_base = float(item_dict.get('max_receta') or 0) * 2
            stock_act_base = float(item_dict.get('stock_actual_base') or 0)
            
            item_dict['stock_visual'] = stock_act_base / factor
            item_dict['minimo_visual'] = stock_min_base / factor
            item_dict['abr'] = abr.upper()
            item_dict['estado_stock'] = self._obtener_estado_stock(stock_act_base, stock_min_base)
            items_procesados.append(item_dict)

        pagination.items = items_procesados
        pagination.bajo_stock_total = bajo_stock_total
        pagination.sin_stock_total = sin_stock_total
        return pagination

    def _obtener_estado_stock(self, actual, minimo):
        if actual <= 0: 
            return "sin_stock"
        if actual < minimo: 
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