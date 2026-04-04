from app.modules.unidades_medida import repository
from app.modules.unidades_medida.model import UnidadMedida

class UnidadMedidaService:
    def listar_unidades_medida(self):
        return repository.get_all_unidad_medida()

    def obtener_unidad_medida(self, id):
        unidad = repository.get_unidad_medida_by_id(id)
        if not unidad:
            raise ValueError("La unidad de medida no existe.")
        return unidad

    def obtener_unidades_base_por_tipo(self, tipo):
        return repository.get_unidades_base_por_tipo(tipo)

    def crear_unidad_medida(self, nombre, abreviatura, tipo, es_base, unidad_base_id, valor_conversion):
        if repository.get_unidad_medida_by_nombre(nombre):
            raise ValueError(f"La unidad '{nombre}' ya existe.")
        
        if not es_base and (not unidad_base_id or not valor_conversion):
            raise ValueError("Las unidades derivadas requieren una unidad base y un valor de conversión.")

        nueva = UnidadMedida(
            nombre=nombre.strip(),
            abreviatura=abreviatura.strip(),
            tipo=tipo,
            es_base=es_base,
            unidad_base_id=unidad_base_id if not es_base else None,
            valor_conversion=valor_conversion if not es_base else None
        )
        return repository.create_unidad_medida(nueva)

    def actualizar_unidad_medida(self, id, nombre, abreviatura, tipo, es_base, unidad_base_id, valor_conversion):
        unidad = repository.get_unidad_medida_by_id(id)
        if not unidad:
            raise ValueError("No encontrada.")

        unidad.nombre = nombre.strip()
        unidad.abreviatura = abreviatura.strip()
        unidad.tipo = tipo
        unidad.es_base = es_base
        unidad.unidad_base_id = unidad_base_id if not es_base else None
        unidad.valor_conversion = valor_conversion if not es_base else None
        
        repository.update_db()
        return unidad

    def eliminar_unidad_medida(self, id):
        unidad = repository.get_unidad_medida_by_id(id)
        if unidad:
            repository.delete_unidad_medida(unidad)