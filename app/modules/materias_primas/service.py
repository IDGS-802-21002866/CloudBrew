from app.modules.materias_primas import repository
from app.modules.materias_primas.model import MateriaPrima

class MateriaPrimaService:
    @staticmethod
    def listar_materias(incluir_inactivas=True):
        if incluir_inactivas:
            return repository.get_all_materias_primas_with_inactive()
        return repository.get_all_materias_primas_activas()

    @staticmethod
    def obtener_por_id(id):
        materia = repository.get_materia_prima_by_id(id)
        if not materia: raise ValueError("Materia prima no encontrada.")
        return materia

    @staticmethod
    def crear_materia(data):
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
        return repository.create_materia_prima(nueva)
    
    @staticmethod
    def desactivar_materia(id):
        materia = repository.get_materia_prima_by_id(id)
        if materia and materia.activo:
            materia.activo = False
            repository.update_db()
        elif materia and not materia.activo:
            raise ValueError("La materia prima ya está desactivada.")

    @staticmethod
    def activar_materia(id): # NUEVO
        materia = repository.get_materia_prima_by_id(id)
        if materia and not materia.activo:
            materia.activo = True
            repository.update_db()
        elif materia and materia.activo:
            raise ValueError("La materia prima ya está activa.")