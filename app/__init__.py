from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager

from app.core.config import DevelopmentConfig


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

login_manager = LoginManager()


def create_app():
    import app.modules
    from app.modules.auth import bp as auth_bp
    from app.modules.main import bp as main_bp

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        from app.modules.usuarios.repository import getUsuarioById

        return getUsuarioById(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
