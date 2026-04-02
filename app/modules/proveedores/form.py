from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


class ProveedorForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(max=100, message="Máximo 100 caracteres")
        ]
    )
    telefono = StringField(
        "Teléfono",
        validators=[
            Optional(),
            Length(max=20, message="Máximo 20 caracteres")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            Optional(),
            Email(message="Correo electrónico inválido"),
            Length(max=100)
        ]
    )
    direccion = StringField(
        "Dirección",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )