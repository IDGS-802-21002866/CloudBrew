from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager, login_required
from werkzeug import security

from app.core.config import DevelopmentConfig


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

login_manager = LoginManager()
migrate = Migrate()


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
    from app.modules.recetas import bp as recetas_bp
    from app.modules.inventario_materias_primas import (
        bp as inventario_materias_primas_bp,
    )
    from app.modules.inventario_producto_terminado import (
        bp as inventario_producto_terminado_bp,
    )

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        from app.modules.usuarios.repository import getUsuarioById

        usuario = getUsuarioById(int(user_id))
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
        compras_bp,
        clientes_bp,
        proc_prod_bp,
        recetas_bp,
        inventario_materias_primas_bp,
        inventario_producto_terminado_bp,
    ]

    for bp in blueprints_protegidos:
        bp.before_request(login_required(lambda: None))

    app.register_blueprint(auth_bp)
    for bp in blueprints_protegidos:
        app.register_blueprint(bp)

    return app
