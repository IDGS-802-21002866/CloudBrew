from app.modules.usuarios.model import Usuario


def getUsuarioByEmail(email):
    return Usuario.query.filter(Usuario.email == email).first()


def getUsuarioById(id):
    return Usuario.query.get(id)
