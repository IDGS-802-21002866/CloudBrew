from dotenv import load_dotenv

load_dotenv()

from app import create_app, db

app = create_app()

# TODO: QUITAR ESTO DESPUES DE CREAR EL USUARIO DE PRUEBA, SOLO PARA TESTING
# Crear usuario de prueba
with app.app_context():
    from app.modules.usuarios.model import Usuario
    from werkzeug.security import generate_password_hash

    # Verificar si el usuario de prueba existe
    usuario_test = Usuario.query.filter_by(email="test@test.com").first()

    if not usuario_test:
        usuario_test = Usuario(
            nombre="Usuario de Prueba",
            email="test@test.com",
            password=generate_password_hash("123456"),
            rol="admin",
            activo=True,
        )
        db.session.add(usuario_test)
        db.session.commit()
        print("Usuario de prueba creado: test@test.com / 123456")
    else:
        print("Usuario de prueba ya existe")

if __name__ == "__main__":
    app.run()
