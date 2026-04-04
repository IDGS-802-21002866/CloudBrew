from dotenv import load_dotenv

load_dotenv()

from app import create_app, db

app = create_app()

# TODO: QUITAR ESTO DESPUES DE CREAR EL USUARIO DE PRUEBA, SOLO PARA TESTING
# Crear usuario de prueba
with app.app_context():
    from app.modules.usuarios.model import Rol, Usuario
    from werkzeug.security import generate_password_hash

    # Verificar si el rol admin existe
    rol_admin = Rol.query.filter_by(name="admin").first()

    if not rol_admin:
        rol_admin = Rol(name="admin", description="Administrador del sistema")
        db.session.add(rol_admin)
        db.session.commit()
        print("Rol admin creado")
    else:
        print("Rol admin ya existe")

    # Verificar si el usuario de prueba existe
    usuario_test = Usuario.query.filter_by(email="test@test.com").first()

    if not usuario_test:
        usuario_test = Usuario(
            nombre="Usuario de Prueba",
            email="test@test.com",
            password=generate_password_hash("123456"),
            rol=rol_admin,
            activo=True,
        )
        db.session.add(usuario_test)
        db.session.commit()
        print("Usuario de prueba creado: test@test.com / 123456")
    else:
        # Asegura que el usuario tenga asignado el rol admin
        if usuario_test.rol != rol_admin:
            usuario_test.rol = rol_admin
            db.session.commit()
            print("Rol admin asignado al usuario de prueba")
        print("Usuario de prueba ya existe")

if __name__ == "__main__":
    app.run()
