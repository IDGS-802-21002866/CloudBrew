from dotenv import load_dotenv

load_dotenv()

from app import create_app, db

app = create_app()

# TODO: QUITAR ESTO DESPUES DE CREAR EL USUARIO DE PRUEBA, SOLO PARA TESTING
# Crear usuario de prueba
with app.app_context():
    from app.modules.usuarios.model import Rol, Usuario
    from app.modules.unidades_medida.model import TipoMedida, UnidadMedida
    from werkzeug.security import generate_password_hash

    # Roles a crear
    roles_data = [
        {"name": "admin", "description": "Administrador del sistema"},
        {"name": "almacen", "description": "Encargado de almacén"},
        {"name": "compras", "description": "Encargado de compras"},
        {"name": "ventas", "description": "Encargado de ventas"},
        {"name": "cliente", "description": "Cliente del portal web"},
    ]

    # Crear roles
    rol_admin = None
    for rol_data in roles_data:
        rol_existente = Rol.query.filter_by(name=rol_data["name"]).first()
        if not rol_existente:
            nuevo_rol = Rol(name=rol_data["name"], description=rol_data["description"])
            db.session.add(nuevo_rol)
            db.session.commit()
            print(f"Rol '{rol_data['name']}' creado")
            if rol_data["name"] == "admin":
                rol_admin = nuevo_rol
        else:
            print(f"Rol '{rol_data['name']}' ya existe")
            if rol_data["name"] == "admin":
                rol_admin = rol_existente

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

    # Crear TipoMedida y UnidadMedida base
    tipos_datos = [
        {"nombre": "Masa", "unidad_base": "Gramos"},
        {"nombre": "Volumen", "unidad_base": "Litros"},
        {"nombre": "Pieza", "unidad_base": "Piezas"},
    ]

    unidades_base_datos = [
        {"nombre": "Gramos", "abreviatura": "g", "tipo": "Masa", "conversion": 1.0},
        {"nombre": "Litros", "abreviatura": "L", "tipo": "Volumen", "conversion": 1.0},
        {"nombre": "Piezas", "abreviatura": "pz", "tipo": "Pieza", "conversion": 1.0},
    ]

    # Crear tipos de medida
    for tipo_data in tipos_datos:
        tipo_existente = TipoMedida.query.filter_by(nombre=tipo_data["nombre"]).first()
        if not tipo_existente:
            nuevo_tipo = TipoMedida(
                nombre=tipo_data["nombre"], unidad_base=tipo_data["unidad_base"]
            )
            db.session.add(nuevo_tipo)
            db.session.commit()
            print(f"TipoMedida '{tipo_data['nombre']}' creado")
        else:
            print(f"TipoMedida '{tipo_data['nombre']}' ya existe")

    # Crear unidades base del sistema
    for unidad_data in unidades_base_datos:
        unidad_existente = UnidadMedida.query.filter_by(
            nombre=unidad_data["nombre"]
        ).first()
        if not unidad_existente:
            tipo = TipoMedida.query.filter_by(nombre=unidad_data["tipo"]).first()
            if tipo:
                nueva_unidad = UnidadMedida(
                    nombre=unidad_data["nombre"],
                    abreviatura=unidad_data["abreviatura"],
                    tipo_medida_id=tipo.id,
                    valor_conversion=unidad_data["conversion"],
                    es_base_sistema=True,
                )
                db.session.add(nueva_unidad)
                db.session.commit()
                print(f"UnidadMedida base '{unidad_data['nombre']}' creada")
        else:
            print(f"UnidadMedida '{unidad_data['nombre']}' ya existe")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
