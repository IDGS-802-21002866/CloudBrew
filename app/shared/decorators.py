from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def require_role(*roles):
    """
    Decorador que requiere que el usuario tenga uno de los roles especificados.

    Uso:
        @bp.route("/admin")
        @require_role("admin")
        def admin_panel():
            return "Bienvenido admin"

        @bp.route("/dashboard")
        @require_role("admin", "gerente")  # Acepta múltiples roles
        def dashboard():
            return "Bienvenido"
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar que el usuario esté autenticado
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión para acceder a este recurso", "warning")
                return redirect(url_for("auth.login"))

            # Verificar que el usuario tenga un rol asignado
            if not current_user.rol:
                flash("Tu usuario no tiene un rol asignado", "danger")
                return redirect(url_for("main.index"))

            # Verificar que el rol del usuario esté en los roles permitidos
            if current_user.rol.name not in roles:
                flash(
                    f"No tienes permiso para acceder a este recurso.",
                    "danger",
                )
                return redirect(url_for("main.index"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def login_required(f):
    """
    Decorador que requiere que el usuario esté autenticado.

    Uso:
        @bp.route("/")
        @login_required
        def index():
            return "Página protegida"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Debes iniciar sesión", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def has_role(role_name):
    """
    Función para verificar si el usuario actual tiene un rol específico.
    Útil en templates y en lógica de negocio.

    Uso en rutas:
        if has_role("admin"):
            # Hacer algo solo para admins

    Uso en templates:
        {% if current_user.rol and current_user.rol.name == "admin" %}
            <a href="/admin">Panel Admin</a>
        {% endif %}
    """
    if not current_user.is_authenticated:
        return False

    if not current_user.rol:
        return False

    return current_user.rol.name == role_name
