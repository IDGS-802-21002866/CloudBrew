from flask import flash, render_template, request
from . import bp
from .service import BitacoraLoginService
from app.shared.decorators import login_required

bitacora_service = BitacoraLoginService()

@login_required
@bp.route("/", methods=["GET"])
def listar():
    try:
        pag = bitacora_service.obtener_bitacoras_login_paginadas(
        pagina=request.args.get("page", 1, type=int),
        por_pagina=request.args.get("per_page", 5, type=int),
        )
        bitacora = pag.items
        pagination = {
            "page": pag.page,
            "pages": list(range(1, pag.pages + 1)),
            "has_prev": pag.has_prev,
            "has_next": pag.has_next,
            "prev_num": pag.prev_num,
            "next_num": pag.next_num,
            "total": pag.total,
            "start": (pag.page - 1) * pag.per_page + 1 if pag.total > 0 else 0,
            "end": min(pag.page * pag.per_page, pag.total),
        }
        return render_template("bitacora_lista.html", pagination=pagination, bitacora=bitacora)
    except ValueError as e:
        flash(str(e), "danger")
        return render_template("bitacora_lista.html", pagination=None, bitacora=[])