import os
from datetime import date, datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
import pymysql

load_dotenv()


def _get_conexion():
    db_url = os.getenv("DATABASE_URL")
    parsed = urlparse(db_url)

    DB_USER = parsed.username
    DB_PASSWORD = parsed.password
    DB_HOST = parsed.hostname
    DB_PORT = parsed.port or 3306
    DB_NAME = parsed.path.lstrip("/")

    return (
        pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
        ),
        DB_NAME,
    )


def backup_db(path: str = "backups"):
    os.makedirs(path, exist_ok=True)

    conn, db_name = _get_conexion()
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = os.path.join(path, f"{db_name}_{fecha}.sql")

    try:
        with open(filepath, "w", encoding="utf-8") as f, conn.cursor() as cursor:
            f.write(f"-- Respaldo de {db_name} generado el {fecha}\n")
            f.write("SET FOREIGN_KEY_CHECKS=0;\n")
            f.write("SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='';\n\n")

            cursor.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = %s AND table_type = 'BASE TABLE'",
                (db_name,),
            )
            tablas = [row[0] for row in cursor.fetchall()]

            for tabla in tablas:
                cursor.execute(f"SHOW CREATE TABLE `{tabla}`")
                create_stmt = cursor.fetchone()[1]
                f.write(f"DROP TABLE IF EXISTS `{tabla}`;\n")
                f.write(f"{create_stmt};\n\n")

                cursor.execute(f"SELECT * FROM `{tabla}`")
                filas = cursor.fetchall()
                if filas:
                    columnas = [desc[0] for desc in cursor.description]
                    cols_str = ", ".join(f"`{c}`" for c in columnas)
                    for fila in filas:
                        valores = ", ".join(
                            "NULL" if v is None else f"'{conn.escape_string(str(v))}'"
                            for v in fila
                        )
                        f.write(
                            f"INSERT INTO `{tabla}` ({cols_str}) VALUES ({valores});\n"
                        )
                    f.write("\n")
            # --- VISTAS ---
            cursor.execute(
                "SELECT table_name FROM information_schema.views "
                "WHERE table_schema = %s",
                (db_name,),
            )
            vistas = [row[0] for row in cursor.fetchall()]

            if vistas:
                f.write("-- VISTAS\n")
                for vista in vistas:
                    cursor.execute(f"SHOW CREATE VIEW `{vista}`")
                    row = cursor.fetchone()
                    create_view = row[1]
                    f.write(f"DROP VIEW IF EXISTS `{vista}`;\n")
                    f.write(f"{create_view};\n\n")

            # --- TRIGGERS ---
            cursor.execute(
                "SELECT trigger_name FROM information_schema.triggers "
                "WHERE trigger_schema = %s",
                (db_name,),
            )
            triggers = [row[0] for row in cursor.fetchall()]

            if triggers:
                f.write("-- TRIGGERS\n")
                for trigger in triggers:
                    cursor.execute(f"SHOW CREATE TRIGGER `{trigger}`")
                    row = cursor.fetchone()
                    create_trigger = row[2]
                    f.write(f"DROP TRIGGER IF EXISTS `{trigger}`;\n")
                    f.write(f"DELIMITER ;;\n{create_trigger} ;;\nDELIMITER ;\n\n")

            f.write("SET FOREIGN_KEY_CHECKS=1;\n")
            f.write("SET SQL_MODE=@OLD_SQL_MODE;\n")

    finally:
        conn.close()

    return filepath


def restore_db(sql_file_path: str):
    if not os.path.exists(sql_file_path):
        raise FileNotFoundError("Archivo no encontrado")
    if not sql_file_path.endswith(".sql"):
        raise ValueError("Archivo inválido")

    conn, _ = _get_conexion()
    try:
        with open(sql_file_path, "r", encoding="utf-8") as f:
            contenido = f.read()

        # Separar sentencias por ; ignorando comentarios
        sentencias = [
            s.strip()
            for s in contenido.split(";")
            if s.strip() and not s.strip().startswith("--")
        ]

        with conn.cursor() as cursor:
            for sentencia in sentencias:
                if sentencia:
                    cursor.execute(sentencia)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise ValueError(f"Error al restaurar: {e}")
    finally:
        conn.close()

    return True
