from app.modules.unidades_medida import repository
from app.modules.unidades_medida.model import UnidadMedida, TipoMedida
from app.shared.exceptions import ValidacionNegocioException
from flask_login import current_user


class UnidadMedidaService:
    def listar_unidades_medida(self):
        return repository.get_all_unidad_medida()
    
    def listar_unidades_medida(self, page, per_page, search_term=None, incluir_inactivas=False):
        return repository.get_paginated_unidad_medida(
        page=page,
        per_page=per_page,
        search_term=search_term,
        incluir_inactivas=incluir_inactivas
        )

    def listar_tipos_medida(self):
        return repository.get_all_tipo_medida()

    def obtener_unidad_medida(self, id):
        unidad = repository.get_unidad_medida_by_id(id)
        if not unidad:
            raise ValueError("La unidad de medida no existe.")
        return unidad

    def obtener_tipo_medida(self, id):
        tipo = repository.get_tipo_medida_by_id(id)
        if not tipo:
            raise ValueError("El tipo de medida no existe.")
        return tipo

    def listar_unidades_por_tipo(self, tipo_medida_id):
        return repository.get_unidades_by_tipo_medida_id(tipo_medida_id)

    def obtener_unidad_base_por_tipo(self, tipo_medida_id):
        unidad = repository.get_unidad_base_by_tipo_medida_id(tipo_medida_id)
        if not unidad:
            raise ValueError("No se encontró unidad base para este tipo de medida.")
        return unidad

    def crear_unidad_medida(
        self, nombre, abreviatura, tipo_medida_id, valor_conversion=1.0
    ):
        if repository.get_unidad_medida_by_nombre(nombre):
            raise ValueError(f"La unidad '{nombre}' ya existe.")

        if repository.get_unidad_medida_by_abreviatura(abreviatura):
            raise ValueError(f"La abreviatura '{abreviatura}' ya existe.")

        tipo = repository.get_tipo_medida_by_id(tipo_medida_id)
        if not tipo:
            raise ValueError("El tipo de medida no existe.")

        nueva = UnidadMedida(
            nombre=nombre.strip(),
            abreviatura=abreviatura.strip(),
            tipo_medida_id=tipo_medida_id,
            valor_conversion=float(valor_conversion) if valor_conversion else 1.0,
            usuario_id=current_user.id if current_user.is_authenticated else None,
        )
        return repository.create_unidad_medida(nueva)

    def actualizar_unidad_medida(
        self, id, nombre, abreviatura, tipo_medida_id, valor_conversion=1.0
    ):
        unidad = repository.get_unidad_medida_by_id(id)
        if not unidad:
            raise ValueError("Unidad no encontrada.")

        # Proteger unidades base del sistema
        if unidad.es_base_sistema:
            raise ValueError("No se pueden editar las unidades base del sistema.")

        # Validar nombre único (si cambió)
        if nombre.strip() != unidad.nombre:
            if repository.get_unidad_medida_by_nombre(nombre):
                raise ValueError(f"La unidad '{nombre}' ya existe.")

        # Validar abreviatura única (si cambió)
        if abreviatura.strip() != unidad.abreviatura:
            if repository.get_unidad_medida_by_abreviatura(abreviatura):
                raise ValueError(f"La abreviatura '{abreviatura}' ya existe.")

        tipo = repository.get_tipo_medida_by_id(tipo_medida_id)
        if not tipo:
            raise ValueError("El tipo de medida no existe.")

        unidad.nombre = nombre.strip()
        unidad.abreviatura = abreviatura.strip()
        unidad.tipo_medida_id = tipo_medida_id
        unidad.valor_conversion = float(valor_conversion) if valor_conversion else 1.0
        unidad.usuario_id = (
            current_user.id if current_user.is_authenticated else unidad.usuario_id
        )

        repository.update_unidad_medida(unidad)
        return unidad

    def eliminar_unidad_medida(self, id):
        unidad = repository.get_unidad_medida_by_id(id)
        if not unidad:
            raise ValueError("Unidad no encontrada.")

        # Proteger unidades base del sistema
        if unidad.es_base_sistema:
            raise ValueError("No se puede eliminar una unidad base del sistema.")

        unidad.usuario_id = (
            current_user.id if current_user.is_authenticated else unidad.usuario_id
        )
        repository.deactivate_unidad_medida(unidad)
