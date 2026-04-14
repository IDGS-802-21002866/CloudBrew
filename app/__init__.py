from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager, login_required
from flask_mail import Mail
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha

from app.core.config import DevelopmentConfig


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
captcha = FlaskSessionCaptcha()


def create_app():
    import app.modules
    from app.modules.auth import bp as auth_bp
    from app.modules.main import bp as main_bp
    from app.modules.proveedores import bp as proveedores_bp
    from app.modules.usuarios import bp as usuarios_bp
    from app.modules.unidades_medida import bp as unidades_medida_bp
    from app.modules.materias_primas import bp as materias_primas_bp
    from app.modules.presentaciones import bp as presentaciones_bp
    from app.modules.compras import bp as compras_bp
    from app.modules.clientes import bp as clientes_bp
    from app.modules.proc_prod import bp as proc_prod_bp
    from app.modules.mermas_materia_prima import bp as mermas_materia_prima_bp
    from app.modules.recetas import bp as recetas_bp
    from app.modules.lotes import bp as lotes_bp
    from app.modules.produccion import bp as produccion_bp
    from app.modules.bitacora_login import bp as bitacora_login_bp
    from app.modules.respaldo import bp as backup_bp

    from app.modules.inventario_materias_primas import (
        bp as inventario_materias_primas_bp,
    )
    from app.modules.inventario_producto_terminado import (
        bp as inventario_producto_terminado_bp,
    )
    from app.modules.pedidos import bp as pedidos_bp

    from app.modules.procesos_produccion import bp as procesos_produccion_bp
    from app.modules.ventas import bp as ventas_bp
    from app.modules.costos import bp as costos_bp
    from app.modules.tienda import bp as tienda_bp
    from app.modules.producto_venta import bp as producto_venta_bp

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    app.config["SESSION_SQLALCHEMY"] = db
    Session(app)
    captcha.init_app(app)
    app.jinja_env.globals.update(captcha=captcha)

    migrate.init_app(app, db)
    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        from app.modules.usuarios.repository import get_usuario_by_id

        usuario = get_usuario_by_id(int(user_id))
        # Solo retornar usuario si está activo
        if usuario and usuario.activo:
            return usuario
        return None

    blueprints_protegidos = [
        main_bp,
        proveedores_bp,
        usuarios_bp,
        unidades_medida_bp,
        materias_primas_bp,
        presentaciones_bp,
        proc_prod_bp,
        compras_bp,
        clientes_bp,
        recetas_bp,
        inventario_materias_primas_bp,
        mermas_materia_prima_bp,
        pedidos_bp,
        inventario_producto_terminado_bp,
        lotes_bp,
        produccion_bp,
        procesos_produccion_bp,
        ventas_bp,
        costos_bp,
        bitacora_login_bp,
        backup_bp,
        producto_venta_bp,
    ]

    for bp in blueprints_protegidos:
        bp.before_request(login_required(lambda: None))

    app.register_blueprint(auth_bp)
    app.register_blueprint(tienda_bp)

    for bp in blueprints_protegidos:
        app.register_blueprint(bp)

    @app.after_request
    def no_cache(response):
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    return app
