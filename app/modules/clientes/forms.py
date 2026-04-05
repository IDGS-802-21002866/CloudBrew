from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField
from wtforms.validators import DataRequired, Length, Email, Optional

class ClienteForm(FlaskForm):
    nombres = StringField(
        "Nombres",
        validators=[DataRequired(message="Los nombres son obligatorios."), Length(max=100)]
    )
    apellidos = StringField(
        "Apellidos",
        validators=[DataRequired(message="Los apellidos son obligatorios."), Length(max=100)]
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(message="El email es obligatorio."), Email(message="Email inválido."), Length(max=100)]
    )
    telefono = StringField(
        "Teléfono",
        validators=[Optional(), Length(max=20)]
    )
    calle_numero = StringField(
        "Calle y Número",
        validators=[DataRequired(message="La calle y número son obligatorios."), Length(max=150)]
    )
    colonia = StringField(
        "Colonia",
        validators=[DataRequired(message="La colonia es obligatoria."), Length(max=100)]
    )
    ciudad = StringField(
        "Ciudad",
        validators=[DataRequired(message="La ciudad es obligatoria."), Length(max=100)]
    )
    estado = StringField(
        "Estado",
        validators=[DataRequired(message="El estado es obligatorio."), Length(max=100)]
    )
    codigo_postal = StringField(
        "Código Postal",
        validators=[DataRequired(message="El código postal es obligatorio."), Length(max=10)]
    )
    tipo = SelectField(
        "Tipo",
        choices=[('web', 'Web'), ('retail', 'Retail')],
        validators=[DataRequired(message="Selecciona un tipo.")]
    )