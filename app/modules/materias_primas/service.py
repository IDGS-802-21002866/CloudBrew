from app.modules.materias_primas import repository
from app.modules.materias_primas.model import MateriaPrima

class MateriaPrimaService:
    
    def listar_materias(self, incluir_inactivas=True):
        if incluir_inactivas:
            return repository.get_all_materias_primas_with_inactive()
        return repository.get_all_materias_primas_activas()

    
    def obtener_por_id(self, id):
        materia = repository.get_materia_prima_by_id(id)
        if not materia: raise ValueError("Materia prima no encontrada.")
        return materia

    
    def crear_materia(self, data):
        nombre = data.get("nombre").strip().capitalize()
        if repository.get_materia_prima_by_nombre(nombre):
            raise ValueError(f"La materia prima '{nombre}' ya existe.")
        
        try:
            stock = float(data.get("stock_minimo", 0))
        except (ValueError, TypeError):
            raise ValueError("El stock mínimo debe ser un número válido.")

        if stock < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")

        nueva = MateriaPrima(
            nombre=nombre,
            descripcion=data.get("descripcion"),
            id_unidad_base=data.get("id_unidad_base"),
            stock_minimo=stock
        )
        return repository.create_unidad_medida(nueva) 
    
    
    def desactivar_materia(self, id):
        materia = repository.get_materia_prima_by_id(id)
        if materia and materia.activo:
            materia.activo = False
            repository.update_db()
        elif materia and not materia.activo:
            raise ValueError("La materia prima ya está desactivada.")

    
    def activar_materia(self, id):
        materia = repository.get_materia_prima_by_id(id)
        if materia and not materia.activo:
            materia.activo = True
            repository.update_db()
        elif materia and materia.activo:
            raise ValueError("La materia prima ya está activa.")