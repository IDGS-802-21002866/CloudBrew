from app.modules.recetas import repository
from app.modules.recetas.model import Recetas, RecetaDetalle, ProcesosReceta
from app.modules.materias_primas.model import MateriaPrima
from app.modules.proc_prod.model import ProcesoProductivo
from app.shared.exceptions import ValidacionNegocioException


class RecetaService:
    """Servicio para gestionar recetas, sus detalles y procesos."""

    def listar_recetas(self, incluir_inactivas=True):
        """Lista todas las recetas activas o incluyendo inactivas."""
        if incluir_inactivas:
            return repository.get_all_recetas_with_inactive()
        return repository.get_all_recetas_activas()

    def obtener_receta(self, id):
        """Obtiene una receta por ID."""
        receta = repository.get_receta_by_id(id)
        if not receta:
            raise ValueError("Receta no encontrada.")
        return receta

    def crear_receta(self, data):
        """Crea una nueva receta."""
        nombre = data.get("nombre").strip().capitalize()
        if repository.get_receta_by_nombre(nombre):
            raise ValidacionNegocioException(f"La receta '{nombre}' ya existe.")

        try:
            cantidad = float(data.get("cantidad_producida", 0))
        except (ValueError, TypeError):
            raise ValidacionNegocioException(
                "La cantidad producida debe ser un número válido."
            )

        if cantidad <= 0:
            raise ValidacionNegocioException(
                "La cantidad producida debe ser mayor a 0."
            )

        nueva_receta = Recetas(
            nombre=nombre,
            descripcion=data.get("descripcion"),
            cantidad_producida=cantidad,
            activo=True,
            imagen=data.get("imagen"),
            imagen_tipo=data.get("imagen_tipo"),
        )
        return repository.create_receta(nueva_receta)

    def actualizar_receta(self, id, data):
        """Actualiza una receta existente."""
        receta = self.obtener_receta(id)
        receta.nombre = data.get("nombre").strip().capitalize()
        receta.descripcion = data.get("descripcion")

        try:
            cantidad = float(data.get("cantidad_producida", 0))
        except (ValueError, TypeError):
            raise ValidacionNegocioException(
                "La cantidad producida debe ser un número válido."
            )

        if cantidad <= 0:
            raise ValidacionNegocioException(
                "La cantidad producida debe ser mayor a 0."
            )

        receta.cantidad_producida = cantidad
        if data.get("imagen") is not None:
            receta.imagen = data.get("imagen")
            receta.imagen_tipo = data.get("imagen_tipo")
        repository.update_db()
        return receta

    def desactivar_receta(self, id):
        """Desactiva una receta (eliminación lógica)."""
        receta = repository.get_receta_by_id(id)
        if not receta:
            raise ValueError("Receta no encontrada.")
        if receta.activo:
            receta.activo = False
            repository.update_db()
        else:
            raise ValidacionNegocioException("La receta ya está desactivada.")

    def activar_receta(self, id):
        """Activa una receta desactivada."""
        receta = repository.get_receta_by_id(id)
        if not receta:
            raise ValueError("Receta no encontrada.")
        if not receta.activo:
            receta.activo = True
            repository.update_db()
        else:
            raise ValidacionNegocioException("La receta ya está activa.")

    # Métodos para sesión (carrito de detalles)
    def obtener_carrito_detalles(self, carrito):
        """Transforma los datos del carrito en objetos con información completa."""
        detalles_expandidos = []
        for item in carrito:
            materia_prima = MateriaPrima.query.get(item["materia_prima_id"])
            if materia_prima:
                detalles_expandidos.append(
                    {
                        "materia_prima_id": item["materia_prima_id"],
                        "materia_prima_nombre": materia_prima.nombre,
                        "cantidad": item["cantidad"],
                        "tipo_medida": (
                            materia_prima.tipo_medida.nombre
                            if materia_prima.tipo_medida
                            else ""
                        ),
                    }
                )
        return detalles_expandidos

    def agregar_al_carrito_detalles(self, carrito, materia_prima_id, cantidad):
        """Agrega una materia prima al carrito de detalles."""
        materia_prima = MateriaPrima.query.get(materia_prima_id)
        if not materia_prima:
            raise ValidacionNegocioException("Materia prima no encontrada.")

        try:
            cantidad = float(cantidad)
        except (ValueError, TypeError):
            raise ValidacionNegocioException("La cantidad debe ser un número válido.")

        if cantidad <= 0:
            raise ValidacionNegocioException("La cantidad debe ser mayor a 0.")

        # Verificar si ya existe en el carrito
        existe = False
        for item in carrito:
            if item["materia_prima_id"] == materia_prima_id:
                item["cantidad"] += cantidad
                existe = True
                break

        if not existe:
            carrito.append({"materia_prima_id": materia_prima_id, "cantidad": cantidad})

        return carrito

    def quitar_del_carrito_detalles(self, carrito, idx):
        """Quita una materia prima del carrito de detalles."""
        if 0 <= idx < len(carrito):
            carrito.pop(idx)
        return carrito

    def guardar_detalles_receta(self, receta_id, carrito):
        """Guarda los detalles del carrito a la BD como RecetaDetalle."""
        # Eliminar detalles existentes
        RecetaDetalle.query.filter_by(receta_id=receta_id).delete()

        for item in carrito:
            detalle = RecetaDetalle(
                receta_id=receta_id,
                materia_prima_id=item["materia_prima_id"],
                cantidad=item["cantidad"],
            )
            repository.create_receta_detalle(detalle)

    # Métodos para sesión (carrito de procesos)
    def obtener_carrito_procesos(self, carrito):
        """Transforma los datos del carrito de procesos en objetos con información completa."""
        procesos_expandidos = []
        for item in carrito:
            proceso = ProcesoProductivo.query.get(item["proceso_productivo_id"])
            if proceso:
                procesos_expandidos.append(
                    {
                        "proceso_productivo_id": item["proceso_productivo_id"],
                        "proceso_nombre": proceso.nombre,
                        "tiempo_estimado": item["tiempo_estimado"],
                    }
                )
        return procesos_expandidos

    def agregar_al_carrito_procesos(
        self, carrito, proceso_productivo_id, tiempo_estimado
    ):
        """Agrega un proceso al carrito de procesos."""
        proceso = ProcesoProductivo.query.get(proceso_productivo_id)
        if not proceso:
            raise ValidacionNegocioException("Proceso productivo no encontrado.")

        try:
            tiempo = float(tiempo_estimado)
        except (ValueError, TypeError):
            raise ValidacionNegocioException("El tiempo debe ser un número válido.")

        if tiempo <= 0:
            raise ValidacionNegocioException("El tiempo debe ser mayor a 0.")

        # Verificar si ya existe en el carrito
        for item in carrito:
            if item["proceso_productivo_id"] == proceso_productivo_id:
                raise ValidacionNegocioException(
                    "Este proceso ya está asignado a la receta."
                )

        carrito.append(
            {"proceso_productivo_id": proceso_productivo_id, "tiempo_estimado": tiempo}
        )
        return carrito

    def quitar_del_carrito_procesos(self, carrito, idx):
        """Quita un proceso del carrito de procesos."""
        if 0 <= idx < len(carrito):
            carrito.pop(idx)
        return carrito

    def guardar_procesos_receta(self, receta_id, carrito):
        """Guarda los procesos del carrito a la BD como ProcesosReceta."""
        # Eliminar procesos existentes
        ProcesosReceta.query.filter_by(receta_id=receta_id).delete()

        for idx, item in enumerate(carrito, start=1):
            proceso = ProcesosReceta(
                receta_id=receta_id,
                proceso_productivo_id=item["proceso_productivo_id"],
                tiempo_estimado=item["tiempo_estimado"],
                orden=idx,
            )
            repository.create_proceso_receta(proceso)
