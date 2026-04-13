from app.modules.bitacora_login.repository import (
    crear_bitacora_login,
    get_bitacora_login_by_id,
    get_bitacoras_login_paginadas,
    get_all_bitacoras_login,
)


class BitacoraLoginService:

    def crear_bitacora_login(self, nombre_usuario, descripcion=None, auth=False):
        return crear_bitacora_login(nombre_usuario, descripcion, auth)

    def obtener_bitacora_login_por_id(self, id_bitacora):
        return get_bitacora_login_by_id(id_bitacora)

    def obtener_bitacoras_login_paginadas(self, pagina=1, por_pagina=10):
        return get_bitacoras_login_paginadas(pagina, por_pagina)

    def obtener_todas_bitacoras_login(self, pagina=1, por_pagina=10):
        return get_all_bitacoras_login(pagina, por_pagina)
