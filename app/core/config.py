from datetime import timedelta
import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Configuración base compartida por todos los ambientes"""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    CAPTCHA_ENABLE = True
    CAPTCHA_LENGTH = 5
    CAPTCHA_WIDTH = 200
    CAPTCHA_HEIGHT = 160
    SESSION_TYPE = "sqlalchemy"
    SESSION_SQLALCHEMY_TABLE = "session"
    CAPTCHA_INCLUDE_NUMERIC = True
    CAPTCHA_INCLUDE_ALPHABET = False


class DevelopmentConfig(Config):
    """Configuración para desarrollo local"""

    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")


class ProductionConfig(Config):
    """Configuración para producción en Railway"""

    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Solo HTTPS
    # Priorizar MYSQL_URL de Railway, fallback a DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get("MYSQL_URL") or os.environ.get(
        "DATABASE_URL"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    BASE_URL = os.environ.get("BASE_URL")  # Debe estar seteado en Railway
