from . import bp
from flask import flash, redirect, render_template, request, url_for
from .service import LoteProduccionService
from app.shared.decorators import verificar_rol_o_denegar


@bp.before_request
def verificar_acceso():
    return verificar_rol_o_denegar("admin", "almacen")


loteService = LoteProduccionService()


@bp.route("/")
def listar():
    page = request.args.get("page", 1, type=int)
    querry = request.args.get("querry", "", type=str)
    pag = loteService.obtener_lotes_paginados(page=page, per_page=5, querry=querry)
    lotes = pag.items
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
    return render_template("lista.html", lotes=lotes, pagination=pagination)


@bp.route("/<int:id>")
def detalle(id):
    try:
        lote = loteService.obtener(id)
        return render_template(
            "detalle.html",
            lote=lote,
            produccion=lote.produccion,
            procesos=lote.produccion.procesos,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("lotes.listar"))
