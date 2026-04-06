from werkzeug.security import generate_password_hash

from app.modules.usuarios.model import Usuario
from app import db


def get_usuarios(pagina=1, por_pagina=5):
    usuarios = Usuario.query.filter_by(activo=True).paginate(
        page=pagina, per_page=por_pagina, error_out=False
    )
    if not usuarios.items:
        raise ValueError("No hay usuarios activos registrados")
    return usuarios


def getUsuarioByEmail(email):
    usuario = Usuario.query.filter(Usuario.email == email).first()
    return usuario


def getUsuarioById(id):
    usuario = Usuario.query.get(id)
    return usuario


def insertar_usuario(form):
    try:
        existente = Usuario.query.filter(Usuario.email == form.email.data).first()
        if existente:
            raise ValueError("Ya existe un usuario con ese email")

        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            rol=form.rol.data,
            activo=form.activo.data if hasattr(form, "activo") else True,
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario
    except ValueError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise ValueError("Error inesperado al insertar usuario")


def modificar_usuario(id_usuario, form):
    try:
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            raise ValueError(f"No existe un usuario con id {id_usuario}")

        if not usuario.activo:
            raise ValueError(f"El usuario con id {id_usuario} está inactivo")
        if form.email.data != usuario.email:
            existente = Usuario.query.filter(Usuario.email == form.email.data).first()
            if existente:
                raise ValueError("Ya existe un usuario con ese email")

        usuario.nombre = form.nombre.data
        usuario.email = form.email.data
        usuario.rol = form.rol.data

        if form.password.data:
            usuario.password = generate_password_hash(form.password.data)

        db.session.commit()

        return usuario

    except ValueError:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error inesperado al modificar usuario")


def eliminar_usuario(id_usuario):
    try:
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            raise ValueError(f"No existe un usuario con id {id_usuario}")

        if not usuario.activo:
            raise ValueError(f"El usuario con id {id_usuario} ya está inactivo")

        usuario.activo = False
        db.session.commit()

        return True

    except ValueError:
        db.session.rollback()
        raise

    except Exception as e:
        db.session.rollback()
        raise ValueError("Error inesperado al eliminar usuario")
