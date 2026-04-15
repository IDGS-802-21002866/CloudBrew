from app.modules.clientes.model import Cliente
from app import db

def get_all_clientes():
    return Cliente.query.all()

def get_cliente_by_id(id):
    return Cliente.query.get(id)

def get_cliente_by_email(email):
    return Cliente.query.filter(Cliente.email == email).first()

def create_cliente(cliente):
    db.session.add(cliente)
    db.session.commit()
    return cliente

def update_db():
    db.session.commit()

def update_cliente(cliente):
    db.session.commit()

def deactivate_cliente(cliente):
    cliente.activo = False
    db.session.commit()

def get_paginated_clientes(page, per_page, search_term=None):
    query = Cliente.query
    
    if search_term:
        query = query.filter(
            (Cliente.nombres.ilike(f"%{search_term}%")) | 
            (Cliente.apellidos.ilike(f"%{search_term}%"))
        )
        
    return query.order_by(Cliente.fecha_registro.desc()).paginate(page=page, per_page=per_page)