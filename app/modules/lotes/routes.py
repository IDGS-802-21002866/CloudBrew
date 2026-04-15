from . import bp
from flask import flash, redirect, render_template, request, url_for
from .service import LoteProduccionService
from app.shared.decorators import login_required
loteService = LoteProduccionService()

@login_required
@bp.route('/')
def listar():
    page = request.args.get("page", 1, type=int)
    pag = loteService.obtener_lotes_paginados(page=page, per_page=5, querry=None)
    return render_template('lista.html', pagination=pag)
@login_required
@bp.route('/<int:id>')
def detalle(id):
    try:
        lote = loteService.obtener(id)
        return render_template('detalle.html', lote=lote,produccion=lote.produccion,procesos=lote.produccion.procesos)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for('lotes.listar'))