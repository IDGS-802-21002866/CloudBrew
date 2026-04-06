from app.modules.presentaciones import repository
from app.modules.presentaciones.model import Presentacion


class PresentacionService:
    def listar_presentaciones(self, incluir_inactivas=True):
        materias = repository.get_all_presentaciones()
        if incluir_inactivas:
            return materias
        return [m for m in materias if m.activo]

    def obtener_por_id(self, id):
        presentacion = repository.get_presentacion_by_id(id)
        if not presentacion:
            raise ValueError("Presentación no encontrada.")
        return presentacion

    def crear_presentacion(self, data):
        nombre = data.get("nombre").strip().capitalize()
        if repository.get_presentacion_by_nombre(nombre):
            raise ValueError(f"La presentación '{nombre}' ya existe.")

        nueva = Presentacion(
            nombre=nombre,
            tipo_medida_id=data.get("tipo_medida_id"),
            cantidad_equivalente=float(data.get("cantidad_equivalente")),
        )
        return repository.create_presentacion(nueva)

    def actualizar_presentacion(self, id, data):
        p = self.obtener_por_id(id)
        p.nombre = data.get("nombre").strip().capitalize()
        p.tipo_medida_id = data.get("tipo_medida_id")
        p.cantidad_equivalente = float(data.get("cantidad_equivalente"))
        repository.update_db()
        return p

    def desactivar(self, id):
        p = self.obtener_por_id(id)
        p.activo = False
        repository.update_db()

    def activar(self, id):
        p = self.obtener_por_id(id)
        p.activo = True
        repository.update_db()
