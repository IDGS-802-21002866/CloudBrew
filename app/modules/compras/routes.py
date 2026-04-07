from app.modules.auth import bp
from app.modules.compras.service import ComprasService

compras_service = ComprasService()


@bp.route("/")
def listar():
    compras = compras_service.listar_compras()
    return render_template("compras/listar.html", compras=compras)
