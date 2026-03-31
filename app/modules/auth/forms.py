from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, validators, EmailField


class LoginForm(FlaskForm):
    correo = EmailField(
        "Correo",
        [
            validators.DataRequired(message="El correo es requerido"),
            validators.Email(message="El correo no es válido"),
        ],
    )
    contrasenia = PasswordField(
        "Contraseña", [validators.DataRequired(message="La contraseña es requerida")]
    )

    submit = SubmitField("Iniciar sesión")
