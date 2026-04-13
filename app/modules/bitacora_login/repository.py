from app.modules.bitacora_login.model import BitacoraLogin
from app import db


def crear_bitacora_login(nombre_usuario, descripcion=None, auth=False):
    try:
        nueva_bitacora = BitacoraLogin(
            nombre_usuario=nombre_usuario,
            descripcion=descripcion,
            auth=auth
        )
        db.session.add(nueva_bitacora)
        db.session.commit()
        return nueva_bitacora
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error al insertar registro en bitácora de login: {str(e)}")


def get_bitacora_login_by_id(id_bitacora):
    try:
        return BitacoraLogin.query.get(id_bitacora)
    except Exception as e:
        raise ValueError(f"Error al obtener registro de bitácora de login por ID: {str(e)}")


def get_bitacoras_login_paginadas(pagina=1, por_pagina=10):
    try:
        bitacoras = BitacoraLogin.query.paginate(
            page=pagina, per_page=por_pagina, error_out=False
        )
        if not bitacoras.items:
            raise ValueError("No hay registros en la bitácora de login")
        return bitacoras
    except Exception as e:
        raise ValueError(f"Error al obtener la paginación de bitácora de login: {str(e)}")

def get_all_bitacoras_login(pagina=1, por_pagina=10):
    return get_bitacoras_login_paginadas(pagina, por_pagina)
