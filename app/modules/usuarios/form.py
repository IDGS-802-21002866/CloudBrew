from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError
from app.modules.usuarios.model import Usuario

class UsuarioForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres")
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es obligatorio"),
            Email(message="Correo inválido"),
            Length(max=100)
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria"),
            Length(min=6, message="Debe tener al menos 6 caracteres")
        ]
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Confirma la contraseña"),
            EqualTo("password", message="Las contraseñas no coinciden")
        ]
    )

    rol = SelectField(
        "Rol",
        choices=[
            (1, "Administrador"),
            (2, "Compras"),
            (3, "Ventas"),
            (4, "Almacén")
        ],
        validators=[DataRequired(message="El rol es obligatorio")]
    )

class UsuarioFormAux(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres")
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es obligatorio"),
            Email(message="Correo inválido"),
            Length(max=100)
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            Optional(),
            Length(min=6, message="Debe tener al menos 6 caracteres")
        ]
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            Optional(),
            EqualTo("password", message="Las contraseñas no coinciden")
        ]
    )

    rol = SelectField(
        "Rol",
        choices=[
            (1, "Administrador"),
            (2, "Compras"),
            (3, "Ventas"),
            (4, "Almacén")
        ],
        validators=[DataRequired(message="El rol es obligatorio")]
    )