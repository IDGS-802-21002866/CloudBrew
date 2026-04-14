from decimal import Decimal

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    make_response,
)
from app.modules.recetas import bp
from app.modules.recetas.service import RecetaService
from app.modules.recetas.form import RecetaForm, RecetaDetalleForm, ProcesoRecetaForm
from app.modules.materias_primas.service import MateriaPrimaService
from app.modules.proc_prod.service import ProcesoProductivoService
from app.modules.costos import repository as costos_repo
from app.shared.exceptions import ValidacionNegocioException
from app.modules.unidades_medida.service import UnidadMedidaService

receta_service = RecetaService()
materias_primas_service = MateriaPrimaService()
proceso_productivo_service = ProcesoProductivoService()
UnidadMedidaService = UnidadMedidaService()


@bp.route("/")
def listar():
    """Lista todas las recetas"""
    recetas = receta_service.listar_recetas(incluir_inactivas=True)
    return render_template("recetas/listar.html", recetas=recetas)


@bp.route("/crear", methods=["GET", "POST"])
def crear():
    """Crea una nueva receta con detalles y procesos."""
    if request.method == "GET" and request.args.get("nuevo"):
        session.pop("receta_carrito_detalles", None)
        session.pop("receta_carrito_procesos", None)
        session.pop("receta_form_data", None)
        session.modified = True
    receta_form = RecetaForm()
    detalle_form = RecetaDetalleForm()
    proceso_form = ProcesoRecetaForm()

    medidas = UnidadMedidaService.listar_unidades_medida()
    materias_primas = materias_primas_service.listar_materias(incluir_inactivas=False)
    pag_procesos = proceso_productivo_service.listar_procesos()
    procesos = pag_procesos.items if hasattr(pag_procesos, "items") else pag_procesos

    detalle_form.materia_prima_id.choices = [
        (str(mp.id), mp.nombre) for mp in materias_primas
    ]
    detalle_form.medida.choices = [("", "Selecciona una medida")] + [
        (str(m.id), m.nombre) for m in medidas
    ]
    proceso_form.proceso_productivo_id.choices = [
        (str(p.id), p.nombre) for p in procesos
    ]

    if "receta_carrito_detalles" not in session:
        session["receta_carrito_detalles"] = []
    if "receta_carrito_procesos" not in session:
        session["receta_carrito_procesos"] = []

    def _guardar_form_data():
        session["receta_form_data"] = {
            "nombre": request.form.get("h_nombre", ""),
            "cantidad_producida": request.form.get("h_cantidad_producida", ""),
            "descripcion": request.form.get("h_descripcion", ""),
        }
        session.modified = True

    def _render():
        carrito_items = session.get("receta_carrito_detalles", [])
        detalles_carrito = receta_service.obtener_carrito_detalles(carrito_items)
        procesos_carrito = receta_service.obtener_carrito_procesos(
            session.get("receta_carrito_procesos", [])
        )

        costo_ingredientes = 0.0
        mp_sin_costo = []
        for item in carrito_items:
            costo_mp = costos_repo.get_costo_promedio_materia_prima(
                item["materia_prima_id"]
            )
            if costo_mp == 0:
                mp = next(
                    (
                        d
                        for d in detalles_carrito
                        if d["materia_prima_id"] == item["materia_prima_id"]
                    ),
                    None,
                )
                mp_sin_costo.append(mp["materia_prima_nombre"] if mp else "Desconocida")
            costo_ingredientes += costo_mp * item["cantidad"]

        from decimal import Decimal, InvalidOperation

        form_data = session.get("receta_form_data") or {}
        if form_data:
            receta_form.nombre.data = form_data.get("nombre", "")
            receta_form.descripcion.data = form_data.get("descripcion", "")
            try:
                if form_data.get("cantidad_producida"):
                    receta_form.cantidad_producida.data = Decimal(
                        str(form_data["cantidad_producida"])
                    )
            except InvalidOperation:
                pass

        nombre_receta = form_data.get("nombre", "")

        mp_tipos = {mp.id: mp.tipo_medida_id for mp in materias_primas}
        medida_tipos = {m.id: m.tipo_medida_id for m in medidas}

        return render_template(
            "recetas/crear.html",
            receta_form=receta_form,
            detalle_form=detalle_form,
            proceso_form=proceso_form,
            materias_primas=materias_primas,
            procesos=procesos,
            medidas=medidas,
            detalles_carrito=detalles_carrito,
            procesos_carrito=procesos_carrito,
            costo_ingredientes=costo_ingredientes,
            mp_sin_costo=mp_sin_costo,
            nombre_receta=nombre_receta,
            mp_tipos=mp_tipos,
            medida_tipos=medida_tipos,
        )

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "agregar_detalle":
            if not detalle_form.validate_on_submit():
                return _render()
            try:
                carrito = session["receta_carrito_detalles"]
                medida_id = int(detalle_form.medida.data)
                carrito = receta_service.agregar_al_carrito_detalles(
                    carrito,
                    int(detalle_form.materia_prima_id.data),
                    detalle_form.cantidad.data,
                    medida_id,
                )
                session["receta_carrito_detalles"] = carrito
                session.modified = True
                flash("Materia prima agregada al carrito.", "success")
            except ValidacionNegocioException as e:
                flash(str(e), "danger")
            _guardar_form_data()
            return redirect(url_for("recetas.crear"))

        elif accion == "quitar_detalle":
            try:
                idx = request.form.get("idx", type=int)
                carrito = session["receta_carrito_detalles"]
                carrito = receta_service.quitar_del_carrito_detalles(carrito, idx)
                session["receta_carrito_detalles"] = carrito
                session.modified = True
                flash("Materia prima removida del carrito.", "success")
            except ValidacionNegocioException as e:
                flash(str(e), "danger")
            _guardar_form_data()
            return redirect(url_for("recetas.crear"))

        elif accion == "agregar_proceso":
            if not proceso_form.validate_on_submit():
                return _render()
            try:
                carrito = session["receta_carrito_procesos"]
                carrito = receta_service.agregar_al_carrito_procesos(
                    carrito,
                    (
                        int(proceso_form.proceso_productivo_id.data)
                        if proceso_form.proceso_productivo_id.data
                        else None
                    ),
                    proceso_form.tiempo_estimado.data,
                )
                session["receta_carrito_procesos"] = carrito
                session.modified = True
                flash("Proceso agregado al carrito.", "success")
            except ValidacionNegocioException as e:
                flash(str(e), "danger")
            _guardar_form_data()
            return redirect(url_for("recetas.crear"))

        elif accion == "quitar_proceso":
            try:
                idx = request.form.get("idx", type=int)
                carrito = session["receta_carrito_procesos"]
                carrito = receta_service.quitar_del_carrito_procesos(carrito, idx)
                session["receta_carrito_procesos"] = carrito
                session.modified = True
                flash("Proceso removido del carrito.", "success")
            except ValidacionNegocioException as e:
                flash(str(e), "danger")
            _guardar_form_data()
            return redirect(url_for("recetas.crear"))

        elif accion == "finalizar_receta":
            if not receta_form.validate_on_submit():
                return _render()

            carrito_detalles = session.get("receta_carrito_detalles", [])
            if not carrito_detalles:
                flash("Debe agregar al menos una materia prima a la receta.", "danger")
                return _render()
            carrito_procesos = session.get("receta_carrito_procesos", [])
            if not carrito_procesos:
                flash("Debe agregar al menos un proceso a la receta.", "danger")
                return _render()

            try:
                archivo = request.files.get("imagen")
                imagen_bytes = None
                imagen_tipo = None
                if archivo and archivo.filename:
                    imagen_bytes = archivo.read()
                    imagen_tipo = archivo.mimetype

                data = {
                    "nombre": receta_form.nombre.data,
                    "descripcion": receta_form.descripcion.data,
                    "cantidad_producida": receta_form.cantidad_producida.data,
                    "imagen": imagen_bytes,
                    "imagen_tipo": imagen_tipo,
                }
                receta = receta_service.crear_receta(data)

                # Guardar detalles
                receta_service.guardar_detalles_receta(receta.id, carrito_detalles)

                receta_service.guardar_procesos_receta(receta.id, carrito_procesos)

                # Limpiar sesión
                session["receta_carrito_detalles"] = []
                session["receta_carrito_procesos"] = []
                session.pop("receta_carrito_editando_id", None)
                session.pop("receta_form_data", None)
                session.modified = True

                flash("Receta creada exitosamente.", "success")
                return redirect(url_for("recetas.listar"))
            except ValidacionNegocioException as e:
                flash(str(e), "danger")
                return _render()

    return _render()


@bp.route("/<int:id>")
def detalle(id):
    """Muestra el detalle de una receta."""
    try:
        receta = receta_service.obtener_receta(id)
        return render_template("recetas/detalle.html", receta=receta)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("recetas.listar"))


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    """Edita una receta existente."""
    try:
        receta = receta_service.obtener_receta(id)
        receta_form = RecetaForm(obj=receta)
        detalle_form = RecetaDetalleForm()
        proceso_form = ProcesoRecetaForm()

        materias_primas = materias_primas_service.listar_materias(
            incluir_inactivas=False
        )
        medidas = UnidadMedidaService.listar_unidades_medida()
        pag_procesos = proceso_productivo_service.listar_procesos()
        procesos = (
            pag_procesos.items if hasattr(pag_procesos, "items") else pag_procesos
        )
        detalle_form.materia_prima_id.choices = [
            (str(mp.id), mp.nombre) for mp in materias_primas
        ]

        detalle_form.medida.choices = [("", "Selecciona una medida")] + [
            (str(m.id), m.nombre) for m in medidas
        ]

        proceso_form.proceso_productivo_id.choices = [
            (str(p.id), p.nombre) for p in procesos
        ]
        # Inicializar carritos con datos existentes en BD.
        # Si el id de receta en edición cambió (o no existe), recargar desde BD.
        if session.get("receta_carrito_editando_id") != id:
            session["receta_carrito_editando_id"] = id
            session["receta_carrito_detalles"] = [
                {"materia_prima_id": d.materia_prima_id, "cantidad": float(d.cantidad)}
                for d in receta.detalle
            ]
            session["receta_carrito_procesos"] = [
                {
                    "proceso_productivo_id": p.proceso_productivo_id,
                    "tiempo_estimado": float(p.tiempo_estimado),
                }
                for p in receta.procesos_receta
            ]
            session.modified = True
        elif "receta_carrito_detalles" not in session:
            session["receta_carrito_detalles"] = [
                {"materia_prima_id": d.materia_prima_id, "cantidad": float(d.cantidad)}
                for d in receta.detalle
            ]
            session["receta_carrito_procesos"] = [
                {
                    "proceso_productivo_id": p.proceso_productivo_id,
                    "tiempo_estimado": float(p.tiempo_estimado),
                }
                for p in receta.procesos_receta
            ]
            session.modified = True

        def _render():
            carrito_items = session.get("receta_carrito_detalles", [])
            detalles_carrito = receta_service.obtener_carrito_detalles(carrito_items)
            procesos_carrito = receta_service.obtener_carrito_procesos(
                session.get("receta_carrito_procesos", [])
            )
            costo_ingredientes = 0.0
            mp_sin_costo = []
            for item in carrito_items:
                costo_mp = costos_repo.get_costo_promedio_materia_prima(
                    item["materia_prima_id"]
                )
                if costo_mp == 0:
                    mp = next(
                        (
                            d
                            for d in detalles_carrito
                            if d["materia_prima_id"] == item["materia_prima_id"]
                        ),
                        None,
                    )
                    mp_sin_costo.append(
                        mp["materia_prima_nombre"] if mp else "Desconocida"
                    )
                costo_ingredientes += costo_mp * item["cantidad"]
            mp_tipos = {mp.id: mp.tipo_medida_id for mp in materias_primas}
            medida_tipos = {m.id: m.tipo_medida_id for m in medidas}
            return render_template(
                "recetas/editar.html",
                receta=receta,
                receta_form=receta_form,
                detalle_form=detalle_form,
                proceso_form=proceso_form,
                materias_primas=materias_primas,
                procesos=procesos,
                detalles_carrito=detalles_carrito,
                procesos_carrito=procesos_carrito,
                costo_ingredientes=costo_ingredientes,
                mp_sin_costo=mp_sin_costo,
                mp_tipos=mp_tipos,
                medida_tipos=medida_tipos,
                medidas=medidas,
            )

        if request.method == "POST":
            accion = request.form.get("accion")

            if accion == "agregar_detalle":
                if not detalle_form.validate_on_submit():
                    return _render()
                try:
                    carrito = session["receta_carrito_detalles"]
                    medida_id = int(detalle_form.medida.data)
                    carrito = receta_service.agregar_al_carrito_detalles(
                        carrito,
                        int(detalle_form.materia_prima_id.data),
                        detalle_form.cantidad.data,
                        medida_id,
                    )
                    session["receta_carrito_detalles"] = carrito
                    session.modified = True
                    flash("Materia prima agregada al carrito.", "success")
                except ValidacionNegocioException as e:
                    flash(str(e), "danger")
                return redirect(url_for("recetas.editar", id=id))

            elif accion == "quitar_detalle":
                try:
                    idx = request.form.get("idx", type=int)
                    carrito = session["receta_carrito_detalles"]
                    carrito = receta_service.quitar_del_carrito_detalles(carrito, idx)
                    session["receta_carrito_detalles"] = carrito
                    session.modified = True
                    flash("Materia prima removida del carrito.", "success")
                except ValidacionNegocioException as e:
                    flash(str(e), "danger")
                return redirect(url_for("recetas.editar", id=id))

            elif accion == "agregar_proceso":
                if not proceso_form.validate_on_submit():
                    return _render()
                try:
                    carrito = session["receta_carrito_procesos"]
                    carrito = receta_service.agregar_al_carrito_procesos(
                        carrito,
                        (
                            int(proceso_form.proceso_productivo_id.data)
                            if proceso_form.proceso_productivo_id.data
                            else None
                        ),
                        proceso_form.tiempo_estimado.data,
                    )
                    session["receta_carrito_procesos"] = carrito
                    session.modified = True
                    flash("Proceso agregado al carrito.", "success")
                except ValidacionNegocioException as e:
                    flash(str(e), "danger")
                return redirect(url_for("recetas.editar", id=id))

            elif accion == "quitar_proceso":
                try:
                    idx = request.form.get("idx", type=int)
                    carrito = session["receta_carrito_procesos"]
                    carrito = receta_service.quitar_del_carrito_procesos(carrito, idx)
                    session["receta_carrito_procesos"] = carrito
                    session.modified = True
                    flash("Proceso removido del carrito.", "success")
                except ValidacionNegocioException as e:
                    flash(str(e), "danger")
                return redirect(url_for("recetas.editar", id=id))

            elif accion == "actualizar_receta":
                if not receta_form.validate_on_submit():
                    return _render()

                carrito_detalles = session.get("receta_carrito_detalles", [])
                if not carrito_detalles:
                    flash(
                        "Debe agregar al menos una materia prima a la receta.",
                        "danger",
                    )
                    return _render()

                try:
                    archivo = request.files.get("imagen")
                    imagen_bytes = None
                    imagen_tipo = None
                    if archivo and archivo.filename:
                        imagen_bytes = archivo.read()
                        imagen_tipo = archivo.mimetype

                    data = {
                        "nombre": receta_form.nombre.data,
                        "descripcion": receta_form.descripcion.data,
                        "cantidad_producida": receta_form.cantidad_producida.data,
                        "imagen": imagen_bytes,
                        "imagen_tipo": imagen_tipo,
                    }
                    receta_service.actualizar_receta(id, data)

                    # Guardar detalles
                    receta_service.guardar_detalles_receta(id, carrito_detalles)

                    # Guardar procesos
                    carrito_procesos = session.get("receta_carrito_procesos", [])
                    receta_service.guardar_procesos_receta(id, carrito_procesos)

                    # Limpiar sesión
                    session["receta_carrito_detalles"] = []
                    session["receta_carrito_procesos"] = []
                    session.pop("receta_carrito_editando_id", None)
                    session.modified = True

                    flash("Receta actualizada exitosamente.", "success")
                    return redirect(url_for("recetas.detalle", id=id))
                except ValidacionNegocioException as e:
                    flash(str(e), "danger")
                    return _render()

        return _render()
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("recetas.listar"))


@bp.route("/<int:id>/imagen")
def imagen(id):
    """Sirve la imagen de una receta almacenada en BD."""
    try:
        receta = receta_service.obtener_receta(id)
        if not receta.imagen:
            return redirect(url_for("static", filename="img/logo-solo.png"))
        response = make_response(receta.imagen)
        response.headers.set("Content-Type", receta.imagen_tipo or "image/jpeg")
        response.headers.set("Cache-Control", "public, max-age=3600")
        return response
    except ValueError:
        return redirect(url_for("static", filename="img/logo-solo.png"))


@bp.route("/<int:id>/confirmar_desactivar")
def confirmar_desactivar(id):
    """Página de confirmación para desactivar una receta."""
    try:
        receta = receta_service.obtener_receta(id)
        return render_template("recetas/confirmar_desactivar.html", receta=receta)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("recetas.listar"))


@bp.route("/<int:id>/desactivar", methods=["POST"])
def desactivar(id):
    """Desactiva una receta (eliminación lógica)."""
    try:
        receta_service.desactivar_receta(id)
        flash("Receta desactivada correctamente.", "success")
    except (ValueError, ValidacionNegocioException) as e:
        flash(str(e), "danger")

    return redirect(url_for("recetas.listar"))


@bp.route("/<int:id>/activar", methods=["POST"])
def activar(id):
    """Activa una receta desactivada."""
    try:
        receta_service.activar_receta(id)
        flash("Receta activada correctamente.", "success")
    except (ValueError, ValidacionNegocioException) as e:
        flash(str(e), "danger")

    return redirect(url_for("recetas.listar"))
