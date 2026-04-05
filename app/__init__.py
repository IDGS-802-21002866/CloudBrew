from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
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
    from app.modules.usuarios.model import Rol, Usuario

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    migrate.init_app(app, db)
    from app import modules

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

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(proveedores_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(unidades_medida_bp)
    app.register_blueprint(materias_primas_bp)
    app.register_blueprint(presentaciones_bp)

    # aparentemente entorpece el funcionamiento de flask-migrate, así que lo comento por ahora
    # with app.app_context():
    #    db.create_all()

    return app
