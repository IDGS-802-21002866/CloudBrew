from flask import render_template, request, redirect, url_for, flash, session
from app.modules.recetas import bp
from app.modules.recetas.service import RecetaService
from app.modules.recetas.form import RecetaForm, RecetaDetalleForm, ProcesoRecetaForm
from app.modules.materias_primas.service import MateriaPrimaService
from app.modules.proc_prod.service import ProcesoProductivoService
from app.shared.exceptions import ValidacionNegocioException

receta_service = RecetaService()
materias_primas_service = MateriaPrimaService()
proceso_productivo_service = ProcesoProductivoService()


@bp.route("/")
def listar():
    """Lista todas las recetas"""
    recetas = receta_service.listar_recetas(incluir_inactivas=True)
    return render_template("recetas/listar.html", recetas=recetas)


@bp.route("/crear", methods=["GET", "POST"])
def crear():
    """Crea una nueva receta con detalles y procesos."""
    receta_form = RecetaForm()
    detalle_form = RecetaDetalleForm()
    proceso_form = ProcesoRecetaForm()

    materias_primas = materias_primas_service.listar_materias(incluir_inactivas=False)
    procesos = proceso_productivo_service.listar_procesos()

    detalle_form.materia_prima_id.choices = [
        (str(mp.id), mp.nombre) for mp in materias_primas
    ]
    proceso_form.proceso_productivo_id.choices = [
        (str(p.id), p.nombre) for p in procesos
    ]

    if "receta_carrito_detalles" not in session:
        session["receta_carrito_detalles"] = []
    if "receta_carrito_procesos" not in session:
        session["receta_carrito_procesos"] = []

    def _render():
        detalles_carrito = receta_service.obtener_carrito_detalles(
            session.get("receta_carrito_detalles", [])
        )
        procesos_carrito = receta_service.obtener_carrito_procesos(
            session.get("receta_carrito_procesos", [])
        )
        return render_template(
            "recetas/crear.html",
            receta_form=receta_form,
            detalle_form=detalle_form,
            proceso_form=proceso_form,
            materias_primas=materias_primas,
            procesos=procesos,
            detalles_carrito=detalles_carrito,
            procesos_carrito=procesos_carrito,
        )

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "agregar_detalle":
            if not detalle_form.validate_on_submit():
                return _render()
            try:
                carrito = session["receta_carrito_detalles"]
                carrito = receta_service.agregar_al_carrito_detalles(
                    carrito,
                    (
                        int(detalle_form.materia_prima_id.data)
                        if detalle_form.materia_prima_id.data
                        else None
                    ),
                    detalle_form.cantidad.data,
                )
                session["receta_carrito_detalles"] = carrito
                session.modified = True
                flash("Materia prima agregada al carrito.", "success")
            except ValidacionNegocioException as e:
                flash(str(e), "danger")
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
                data = {
                    "nombre": receta_form.nombre.data,
                    "descripcion": receta_form.descripcion.data,
                    "cantidad_producida": receta_form.cantidad_producida.data,
                }
                receta = receta_service.crear_receta(data)

                # Guardar detalles
                receta_service.guardar_detalles_receta(receta.id, carrito_detalles)

                receta_service.guardar_procesos_receta(receta.id, carrito_procesos)

                # Limpiar sesión
                session["receta_carrito_detalles"] = []
                session["receta_carrito_procesos"] = []
                session.pop("receta_carrito_editando_id", None)
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
        procesos = proceso_productivo_service.listar_procesos()

        detalle_form.materia_prima_id.choices = [
            (str(mp.id), mp.nombre) for mp in materias_primas
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
            detalles_carrito = receta_service.obtener_carrito_detalles(
                session.get("receta_carrito_detalles", [])
            )
            procesos_carrito = receta_service.obtener_carrito_procesos(
                session.get("receta_carrito_procesos", [])
            )
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
            )

        if request.method == "POST":
            accion = request.form.get("accion")

            if accion == "agregar_detalle":
                if not detalle_form.validate_on_submit():
                    return _render()
                try:
                    carrito = session["receta_carrito_detalles"]
                    carrito = receta_service.agregar_al_carrito_detalles(
                        carrito,
                        int(detalle_form.materia_prima_id.data),
                        detalle_form.cantidad.data,
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
                    data = {
                        "nombre": receta_form.nombre.data,
                        "descripcion": receta_form.descripcion.data,
                        "cantidad_producida": receta_form.cantidad_producida.data,
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
