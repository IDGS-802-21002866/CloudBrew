from werkzeug.security import generate_password_hash

from app.modules.usuarios.model import Usuario
from app import db

def get_usuarios():
    return Usuario.query.filter_by(activo=True)

def getUsuarioByEmail(email):
    return Usuario.query.filter(Usuario.email == email).first()


def getUsuarioById(id):
    return Usuario.query.get(id)

def insertar_usuario(form):
    try:
        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            rol=form.rol.data,
            activo=form.activo.data if hasattr(form, "activo") else True
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario

    except Exception as e:
        db.session.rollback()
        print(f"Error al insertar usuario: {e}")
        return None

def modificar_usuario(id_usuario, form):
    try:
        usuario = Usuario.query.get(id_usuario)

        if not usuario or not usuario.activo:
            return None

        usuario.nombre = form.nombre.data
        usuario.email = form.email.data
        usuario.rol = form.rol.data

        if form.password.data:
            usuario.password =generate_password_hash(form.password.data)

        db.session.commit()
        return usuario

    except Exception as e:
        db.session.rollback()
        print(f"Error al modificar usuario: {e}")
        return None
    
def eliminar_usuario(id_usuario):
    try:
        usuario = Usuario.query.get(id_usuario)
        if not usuario or not usuario.activo:
            return False
        usuario.activo = False
        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar usuario: {e}")
        return False
