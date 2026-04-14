from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class RegistroClienteForm(FlaskForm):
    nombres = StringField(
        "Nombres",
        [DataRequired(message="Los nombres son obligatorios."), Length(max=100)],
    )
    apellidos = StringField(
        "Apellidos",
        [DataRequired(message="Los apellidos son obligatorios."), Length(max=100)],
    )
    email = EmailField(
        "Email",
        [
            DataRequired(message="El email es obligatorio."),
            Email(message="Email inválido."),
            Length(max=100),
        ],
    )
    telefono = StringField(
        "Teléfono", [Optional(), Length(max=10, message="Máximo 10 dígitos.")]
    )
    contrasenia = PasswordField(
        "Contraseña",
        [
            DataRequired(message="La contraseña es requerida."),
            Length(min=8, message="Mínimo 8 caracteres."),
        ],
    )
    confirmar_contrasenia = PasswordField(
        "Confirmar Contraseña",
        [
            DataRequired(message="Confirma tu contraseña."),
            EqualTo("contrasenia", message="Las contraseñas no coinciden."),
        ],
    )
    calle_numero = StringField(
        "Calle y Número",
        [DataRequired(message="La calle y número son obligatorios."), Length(max=150)],
    )
    colonia = StringField(
        "Colonia",
        [DataRequired(message="La colonia es obligatoria."), Length(max=100)],
    )
    ciudad = StringField(
        "Ciudad",
        [DataRequired(message="La ciudad es obligatoria."), Length(max=100)],
    )
    estado = StringField(
        "Estado",
        [DataRequired(message="El estado es obligatorio."), Length(max=100)],
    )
    codigo_postal = StringField(
        "Código Postal",
        [DataRequired(message="El código postal es obligatorio."), Length(max=10)],
    )
    submit = SubmitField("Completar Registro")


class LoginClienteForm(FlaskForm):
    correo = EmailField(
        "Correo",
        [
            DataRequired(message="El correo es requerido."),
            Email(message="El correo no es válido."),
        ],
    )
    contrasenia = PasswordField(
        "Contraseña",
        [DataRequired(message="La contraseña es requerida.")],
    )
    submit = SubmitField("Iniciar Sesión")


class VerificarCodigoForm(FlaskForm):
    codigo = StringField(
        "Código de Verificación",
        [
            DataRequired(message="El código es requerido."),
            Length(min=6, max=6, message="El código debe ser de 6 dígitos."),
        ],
    )
    submit = SubmitField("Verificar")


class RecuperarContrasenaClienteForm(FlaskForm):
    correo = EmailField(
        "Correo",
        [
            DataRequired(message="El correo es requerido."),
            Email(message="El correo no es válido."),
        ],
    )
    submit = SubmitField("Recuperar contraseña")


class RestablecerContrasenaClienteForm(FlaskForm):
    nueva_contrasenia = PasswordField(
        "Nueva contraseña",
        [
            DataRequired(message="La contraseña es requerida."),
            Length(min=8, message="Mínimo 8 caracteres."),
        ],
    )
    confirmar_contrasenia = PasswordField(
        "Confirmar contraseña",
        [
            DataRequired(message="Confirma tu contraseña."),
            EqualTo("nueva_contrasenia", message="Las contraseñas no coinciden."),
        ],
    )
    submit = SubmitField("Establecer nueva contraseña")
