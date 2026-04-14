import os
import subprocess
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def backup_db(path: str = "backups"):
    mysqldump_path = os.getenv("MYSQLDUMP_PATH", "mysqldump")
    if not os.path.isabs(mysqldump_path) and mysqldump_path != "mysqldump":
        raise ValueError("MYSQLDUMP_PATH debe ser ruta absoluta o 'mysqldump'")
    if mysqldump_path != "mysqldump" and not os.path.exists(mysqldump_path):
        raise FileNotFoundError(f"No se encontró mysqldump en: {mysqldump_path}")
    
    db_url = os.getenv("DATABASE_URL")
    parsed = urlparse(db_url)

    DB_USER = parsed.username
    DB_PASSWORD = parsed.password
    DB_HOST = parsed.hostname
    DB_PORT = parsed.port or 3306
    DB_NAME = parsed.path.lstrip("/")
    os.makedirs(path, exist_ok=True)

    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{DB_NAME}_{fecha}.sql"
    filepath = os.path.join(path, filename)

    command = [
        mysqldump_path,
        "-h", DB_HOST,
        "-P", str(DB_PORT),
        "-u", DB_USER,
        DB_NAME,

        "--extended-insert",
        "--single-transaction",
        "--routines",
        "--triggers",
    ]

    env = os.environ.copy()
    env["MYSQL_PWD"] = DB_PASSWORD

    with open(filepath, "w", encoding="utf-8") as f:
        result = subprocess.run(
            command,
            stdout=f,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )

    if result.returncode != 0:
        raise ValueError(f"Error en backup")

    return filepath

def restore_db(sql_file_path: str):
    if not os.path.exists(sql_file_path):
        raise FileNotFoundError("Archivo no encontrado")

    if not sql_file_path.endswith(".sql"):
        raise ValueError("Archivo inválido")

    mysql_path = os.getenv("MYSQL_PATH", "mysql")

    if mysql_path != "mysql" and not os.path.exists(mysql_path):
        raise FileNotFoundError(f"No se encontró mysql en: {mysql_path}")

    db_url = os.getenv("DATABASE_URL")
    parsed = urlparse(db_url)

    DB_USER = parsed.username
    DB_PASSWORD = parsed.password
    DB_HOST = parsed.hostname
    DB_PORT = parsed.port or 3306
    DB_NAME = parsed.path.lstrip("/")

    env = os.environ.copy()
    env["MYSQL_PWD"] = DB_PASSWORD

    command = [
        mysql_path,
        "-h", DB_HOST,
        "-P", str(DB_PORT),
        "-u", DB_USER,
        DB_NAME
    ]

    with open(sql_file_path, "r", encoding="utf-8") as f:
        result = subprocess.run(
            command,
            stdin=f,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )

    if result.returncode != 0:
        raise ValueError(f"Error al restaurar: {result.stderr}")

    return True

