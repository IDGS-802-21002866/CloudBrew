from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, validators


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


class RecuperarContrasenaForm(FlaskForm):
    correo = EmailField(
        "Correo",
        [
            validators.DataRequired(message="El correo es requerido"),
            validators.Email(message="El correo no es válido"),
        ],
    )
    submit = SubmitField("Recuperar contraseña")


class RestablecerContrasenaForm(FlaskForm):
    nueva_contrasenia = PasswordField(
        "Nueva contraseña",
        [
            validators.DataRequired(message="La contraseña es requerida"),
            validators.Length(min=8, message="Mínimo 8 caracteres"),
        ],
    )
    confirmar_contrasenia = PasswordField(
        "Confirmar contraseña",
        [
            validators.DataRequired(message="Confirma tu contraseña"),
            validators.EqualTo("nueva_contrasenia", message="Las contraseñas no coinciden"),
        ],
    )
    submit = SubmitField("Establecer nueva contraseña")

