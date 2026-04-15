from flask import flash, render_template, request
from . import bp
from .service import BitacoraLoginService
from app.shared.decorators import verificar_rol_o_denegar


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin")


bitacora_service = BitacoraLoginService()


@bp.route("/", methods=["GET"])
def listar():
    try:
        pag = bitacora_service.obtener_bitacoras_login_paginadas(
            pagina=request.args.get("page", 1, type=int),
            por_pagina=request.args.get("per_page", 5, type=int),
        )
        return render_template("bitacora_lista.html", pagination=pag)
    except ValueError as e:
        flash(str(e), "danger")
        return render_template("bitacora_lista.html", pagination=None, bitacora=[])
