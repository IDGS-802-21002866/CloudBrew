from app.modules.lotes.model import LoteProduccion
from app.modules.produccion.model import Produccion
from app.modules.recetas.model import Recetas
from app import db

def insertar_lote_produccion(form):
    try:
        if not form.id_produccion.data:
            raise ValueError("La producción es obligatoria.")

        if not form.codigo_lote.data:
            raise ValueError("El código de lote es obligatorio.")

        lote = LoteProduccion(
            id_produccion=form.id_produccion.data,
            codigo_lote=form.codigo_lote.data,
            fecha_produccion=form.fecha_produccion.data,
            cantidad_generada=form.cantidad_generada.data
        )

        db.session.add(lote)
        db.session.commit()

        return lote

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrió un error al crear el lote de producción.")
def eliminar_lote_produccion(id_lote):
    try:
        lote = LoteProduccion.query.get(id_lote)

        if not lote:
            raise ValueError("El lote no existe.")

        db.session.delete(lote)
        db.session.commit()

        return True

    except ValueError as ve:
        db.session.rollback()
        return ve
    except Exception:
        db.session.rollback()
        return ValueError("Ocurrió un error al eliminar el lote.")

def obtener_lote_produccion(id_lote):
    try:
        lote = LoteProduccion.query.get(id_lote)

        if not lote:
            raise ValueError("El lote no existe.")

        return lote

    except Exception:
        return ValueError("Ocurrió un error al obtener el lote.")
    
def obtener_lotes_por_produccion(id_produccion):
    try:
        lotes = LoteProduccion.query.filter_by(
            id_produccion=id_produccion
        ).all()

        return lotes

    except Exception:
        return ValueError("Ocurrió un error al obtener los lotes.")


def obtener_lotes_por_receta(receta_id):
    try:
        lotes = (
            LoteProduccion.query.join(Produccion)
            .filter(Produccion.id_receta == receta_id)
            .all()
        )
        return lotes
    except Exception:
        return ValueError("Ocurrió un error al obtener los lotes para la receta.")

def listar_lotes_con_paginacion(page=1, per_page=10, querry=""):
    try:
        query = LoteProduccion.query.join(Produccion).join(Recetas)

        if querry:
            busqueda = f"%{querry}%"
            query = query.filter(
                db.or_(
                    LoteProduccion.codigo_lote.ilike(busqueda),
                    Recetas.nombre.ilike(busqueda),
                )
            )

        return query.paginate(page=page, per_page=per_page, error_out=False)
    except Exception:
        return ValueError("Ocurrió un error al obtener los lotes paginados.")