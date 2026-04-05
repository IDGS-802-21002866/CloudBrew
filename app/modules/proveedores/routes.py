from flask import render_template, request, redirect, url_for, flash
from app.modules.proveedores.form import ProveedorForm
from app.modules.proveedores.service import ProveedorService
from . import bp

servicio = ProveedorService()


@bp.route("/")
def listar():
    try:
        # Recibir parámetros de la ruta
        pagina = request.args.get("page", 1, type=int)
        busqueda = request.args.get("q", "", type=str)
        por_pagina = 5

        # Validar paginación
        if pagina < 1:
            pagina = 1

        # Obtener todos los proveedores del servicio
        proveedores = servicio.listar_proveedores(busqueda=busqueda)

        # Validación de presentación (no es lógica de negocio)
        if not proveedores:
            flash("No hay proveedores registrados. Crea uno nuevo.", "info")

        # Paginar en la ruta (presentación)
        total = len(proveedores)
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        proveedores_pagina = proveedores[inicio:fin]

        # Calcular información de paginación
        total_paginas = (total + por_pagina - 1) // por_pagina

        pagination = {
            "page": pagina,
            "pages": list(range(1, total_paginas + 1)),
            "has_prev": pagina > 1,
            "has_next": pagina < total_paginas,
            "prev_num": pagina - 1 if pagina > 1 else None,
            "next_num": pagina + 1 if pagina < total_paginas else None,
            "total": total,
            "start": inicio + 1 if total > 0 else 0,
            "end": min(fin, total),
        }

        return render_template(
            "proveedores/lista_proveedor.html",
            proveedores=proveedores_pagina,
            pagination=pagination,
            busqueda=busqueda,
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("proveedores.listar"))


@bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = ProveedorForm()
    if form.validate_on_submit():
        try:
            datos = {
                "nombre": form.nombre.data,
                "telefono": form.telefono.data,
                "email": form.email.data,
                "direccion": form.direccion.data,
            }
            servicio.crear_proveedor(datos)
            flash("Proveedor creado exitosamente", "success")
            return redirect(url_for("proveedores.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("proveedores/crear.html", form=form)


@bp.route("/<int:id>")
def detalle(id):
    try:
        proveedor = servicio.obtener_proveedor(id)
        return render_template("proveedores/detalle.html", proveedor=proveedor)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("proveedores.listar"))


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    try:
        proveedor = servicio.obtener_proveedor(id)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("proveedores.listar"))

    form = ProveedorForm(obj=proveedor)
    if form.validate_on_submit():
        try:
            datos = {
                "nombre": form.nombre.data,
                "telefono": form.telefono.data,
                "email": form.email.data,
                "direccion": form.direccion.data,
            }
            servicio.actualizar_proveedor(id, datos)
            flash("Proveedor actualizado exitosamente", "success")
            return redirect(url_for("proveedores.listar"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("proveedores/editar.html", form=form, proveedor=proveedor)


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        servicio.eliminar_proveedor(id)
        flash("Proveedor eliminado exitosamente", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("proveedores.listar"))
