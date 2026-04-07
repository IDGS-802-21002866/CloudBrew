from app.modules.compras import repository
from app.modules.materias_primas.service import MateriaPrimaService
from app.modules.presentaciones.service import PresentacionService
from app.shared.exceptions import ValidacionNegocioException

_materias_primas_service = MateriaPrimaService()
_presentaciones_service = PresentacionService()


class ComprasService:
    def listar_compras(self):
        return repository.get_all_compras()

    def agregar_al_carrito(self, carrito, materia_prima_id, presentacion_id, cantidad):
        if not materia_prima_id or not presentacion_id:
            raise ValidacionNegocioException(
                "Materia prima y presentación son requeridas."
            )
        if not cantidad or cantidad <= 0:
            raise ValidacionNegocioException("La cantidad debe ser mayor a 0.")
        if any(d.get("materia_prima_id") == materia_prima_id for d in carrito):
            raise ValidacionNegocioException("Esta materia prima ya fue agregada.")

        carrito.append(
            {
                "materia_prima_id": materia_prima_id,
                "presentacion_id": presentacion_id,
                "cantidad": cantidad,
            }
        )
        return carrito

    def quitar_del_carrito(self, carrito, idx):
        if 0 <= idx < len(carrito):
            carrito.pop(idx)
        return carrito

    def obtener_carrito_con_detalles(self, carrito):
        detalles = []
        for item in carrito:
            materia_prima = _materias_primas_service.obtener_por_id(
                item["materia_prima_id"]
            )
            presentacion = _presentaciones_service.obtener_por_id(
                item["presentacion_id"]
            )
            detalles.append(
                {
                    "materia_prima": materia_prima,
                    "presentacion": presentacion,
                    "cantidad": item["cantidad"],
                }
            )
        return detalles

    def crear_compra(self, proveedor_id, usuario_id, detalles):
        """
        Crear una nueva compra con sus detalles.

        Args:
            proveedor_id: ID del proveedor
            usuario_id: ID del usuario que crea la compra
            detalles: lista de dicts con {materia_prima_id, presentacion_id, cantidad, precio_unitario}

        Returns:
            ID de la compra creada
        """
        if not detalles:
            raise ValueError("Debe agregar al menos un producto a la compra")

        # Validar que no haya materias primas duplicadas
        ids_materias = [d["materia_prima_id"] for d in detalles]
        if len(ids_materias) != len(set(ids_materias)):
            raise ValueError("No se puede agregar la misma materia prima dos veces")

        # Validar que cada detalle tenga campos requeridos
        for detalle in detalles:
            if not detalle.get("materia_prima_id") or not detalle.get("cantidad"):
                raise ValueError("Cada producto debe tener material prima y cantidad")

            try:
                cantidad = float(detalle["cantidad"])
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
            except (ValueError, TypeError):
                raise ValueError("La cantidad debe ser un número válido")

        # Crear compra en base de datos
        compra_id = repository.create_compra(
            proveedor_id=proveedor_id, usuario_id=usuario_id, detalles=detalles
        )

        return compra_id

    def obtener_compra(self, id):
        compra = repository.get_compra_by_id(id)
        if not compra:
            raise ValidacionNegocioException("Compra no encontrada.")
        return compra
