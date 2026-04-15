from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user

from app.modules.tienda import bp
from app.modules.tienda.forms import (
    LoginClienteForm,
    RecuperarContrasenaClienteForm,
    RegistroClienteForm,
    RestablecerContrasenaClienteForm,
    VerificarCodigoForm,
)
from app.modules.tienda.service import (
    TiendaAuthService,
    TiendaCarritoService,
    TiendaCheckoutService,
    TiendaProductoService,
)

auth_service = TiendaAuthService()
producto_service = TiendaProductoService()
carrito_service = TiendaCarritoService()
checkout_service = TiendaCheckoutService()


# ── Contexto global para templates ──────────────────────────────────────────
@bp.context_processor
def inyectar_carrito():
    return {"cantidad_carrito": carrito_service.obtener_cantidad_items()}


# ── Inicio ──────────────────────────────────────────────────────────────────
@bp.route("/")
def inicio():
    productos = producto_service.listar_productos_disponibles()
    return render_template("tienda/inicio.html", productos=productos)


# ── Catálogo ────────────────────────────────────────────────────────────────
@bp.route("/productos")
def listar_productos():
    productos = producto_service.listar_productos_disponibles()
    return render_template("tienda/productos.html", productos=productos)


@bp.route("/producto/<int:id>")
def detalle_producto(id):
    try:
        producto = producto_service.obtener_producto(id)
        return render_template("tienda/producto_detalle.html", producto=producto)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("tienda.listar_productos"))


# ── Autenticación ───────────────────────────────────────────────────────────
@bp.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for("tienda.inicio"))

    form = RegistroClienteForm()
    if form.validate_on_submit():
        try:
            data = {
                "nombres": form.nombres.data,
                "apellidos": form.apellidos.data,
                "email": form.email.data.strip().lower(),
                "telefono": form.telefono.data,
                "contrasenia": form.contrasenia.data,
                "calle_numero": form.calle_numero.data,
                "colonia": form.colonia.data,
                "ciudad": form.ciudad.data,
                "estado": form.estado.data,
                "codigo_postal": form.codigo_postal.data,
            }
            auth_service.registrar_cliente(data)
            flash("¡Registro exitoso! Ya puedes iniciar sesión.", "success")
            return redirect(url_for("tienda.login"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("tienda/registrarse.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("tienda.inicio"))

    form = LoginClienteForm()
    if form.validate_on_submit():
        try:
            auth_service.iniciar_sesion(form.correo.data, form.contrasenia.data)
            flash("Te enviamos un código de verificación a tu correo.", "success")
            return redirect(url_for("tienda.verificar_codigo"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("tienda/login.html", form=form)


@bp.route("/verificar", methods=["GET", "POST"])
def verificar_codigo():
    if current_user.is_authenticated:
        return redirect(url_for("tienda.inicio"))

    if not session.get("codigo_2fa"):
        return redirect(url_for("tienda.login"))

    form = VerificarCodigoForm()
    if form.validate_on_submit():
        try:
            auth_service.verificar_codigo_2fa(form.codigo.data)
            flash("¡Bienvenido!", "success")
            return redirect(url_for("tienda.inicio"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("tienda/verificar_codigo.html", form=form)


@bp.route("/logout")
def logout():
    auth_service.cerrar_sesion()
    flash("Sesión cerrada exitosamente.", "success")
    return redirect(url_for("tienda.inicio"))


@bp.route("/recuperar", methods=["GET", "POST"])
def recuperar_contrasena():
    form = RecuperarContrasenaClienteForm()
    if form.validate_on_submit():
        try:
            auth_service.solicitar_recuperacion(form.correo.data)
            flash("Te enviamos un enlace para recuperar tu contraseña.", "success")
        except ValueError:
            flash("Correo inválido.", "danger")
        return redirect(url_for("tienda.recuperar_contrasena"))

    return render_template("tienda/recuperar_contrasena.html", form=form)


@bp.route("/restablecer/<token>", methods=["GET", "POST"])
def restablecer_contrasena(token):
    form = RestablecerContrasenaClienteForm()
    if form.validate_on_submit():
        try:
            auth_service.restablecer_contrasena(token, form.nueva_contrasenia.data)
            flash("Contraseña actualizada exitosamente.", "success")
            return redirect(url_for("tienda.login"))
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("tienda.recuperar_contrasena"))

    return render_template("tienda/restablecer_contrasena.html", form=form, token=token)


# ── Carrito ─────────────────────────────────────────────────────────────────
@bp.route("/carrito")
def ver_carrito():
    carrito = carrito_service.obtener_carrito()
    total = carrito_service.obtener_total()
    return render_template("tienda/carrito.html", carrito=carrito, total=total)


@bp.route("/carrito/agregar", methods=["POST"])
def agregar_al_carrito():
    producto_venta_id = request.form.get("producto_venta_id", type=int)
    cantidad = request.form.get("cantidad", 1, type=int)

    if not producto_venta_id or cantidad < 1:
        flash("Datos inválidos.", "danger")
        return redirect(request.referrer or url_for("tienda.listar_productos"))

    try:
        carrito_service.agregar_producto(producto_venta_id, cantidad)
        flash("Producto agregado al carrito.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(request.referrer or url_for("tienda.listar_productos"))


@bp.route("/carrito/actualizar", methods=["POST"])
def actualizar_carrito():
    producto_venta_id = request.form.get("producto_venta_id", type=int)
    cantidad = request.form.get("cantidad", type=int)

    if producto_venta_id and cantidad is not None:
        carrito_service.actualizar_cantidad(producto_venta_id, cantidad)

    return redirect(url_for("tienda.ver_carrito"))


@bp.route("/carrito/eliminar/<int:producto_venta_id>", methods=["POST"])
def eliminar_del_carrito(producto_venta_id):
    carrito_service.eliminar_producto(producto_venta_id)
    flash("Producto eliminado del carrito.", "success")
    return redirect(url_for("tienda.ver_carrito"))


# ── Checkout ────────────────────────────────────────────────────────────────
@bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not current_user.is_authenticated:
        flash("Inicia sesión para completar tu compra.", "danger")
        return redirect(url_for("tienda.login"))

    carrito = carrito_service.obtener_carrito()
    total = carrito_service.obtener_total()

    if not carrito:
        flash("Tu carrito está vacío.", "danger")
        return redirect(url_for("tienda.listar_productos"))

    if request.method == "POST":
        try:
            venta = checkout_service.confirmar_compra(current_user)
            flash("¡Compra realizada exitosamente!", "success")
            return redirect(url_for("tienda.confirmacion", venta_id=venta.id))
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("tienda.ver_carrito"))

    from app.modules.tienda.repository import get_cliente_by_email

    cliente = get_cliente_by_email(current_user.email)

    return render_template(
        "tienda/checkout.html", carrito=carrito, total=total, cliente=cliente
    )


@bp.route("/confirmacion/<int:venta_id>")
def confirmacion(venta_id):
    if not current_user.is_authenticated:
        return redirect(url_for("tienda.login"))

    from app.modules.tienda.repository import get_venta_by_id

    venta = get_venta_by_id(venta_id)
    if not venta:
        flash("Venta no encontrada.", "danger")
        return redirect(url_for("tienda.inicio"))

    return render_template("tienda/confirmacion.html", venta=venta)


# ── Cuenta del cliente ──────────────────────────────────────────────────────
@bp.route("/mi-cuenta")
def mi_cuenta():
    if not current_user.is_authenticated:
        flash("Inicia sesión para ver tu cuenta.", "danger")
        return redirect(url_for("tienda.login"))

    from app.modules.tienda.repository import get_cliente_by_email

    cliente = get_cliente_by_email(current_user.email)
    return render_template("tienda/mi_cuenta.html", cliente=cliente)


@bp.route("/mis-compras")
def mis_compras():
    if not current_user.is_authenticated:
        flash("Inicia sesión para ver tus compras.", "danger")
        return redirect(url_for("tienda.login"))

    from app.modules.tienda.repository import (
        get_cliente_by_email,
        get_ventas_by_cliente,
    )

    cliente = get_cliente_by_email(current_user.email)
    ventas = []
    if cliente:
        ventas = get_ventas_by_cliente(cliente.id)

    return render_template("tienda/mis_compras.html", ventas=ventas)
