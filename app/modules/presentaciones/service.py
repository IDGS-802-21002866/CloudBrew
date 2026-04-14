from app.modules.presentaciones import repository
from app.modules.presentaciones.model import Presentacion
from flask_login import current_user


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
            uso=data.get("uso", "comercial"),
            usuario_id=current_user.id if current_user.is_authenticated else None,
        )
        return repository.create_presentacion(nueva)

    def actualizar_presentacion(self, id, data):
        p = self.obtener_por_id(id)
        p.nombre = data.get("nombre").strip().capitalize()
        p.tipo_medida_id = data.get("tipo_medida_id")
        p.cantidad_equivalente = float(data.get("cantidad_equivalente"))
        p.uso = data.get("uso", p.uso)
        p.usuario_id = (
            current_user.id if current_user.is_authenticated else p.usuario_id
        )
        return repository.update_presentacion(p)

    def desactivar(self, id):
        p = self.obtener_por_id(id)
        p.usuario_id = (
            current_user.id if current_user.is_authenticated else p.usuario_id
        )
        return repository.deactivate_presentacion(p)

    def activar(self, id):
        p = self.obtener_por_id(id)
        return repository.activate_presentacion(p)
