from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length


class PresentacionForm(FlaskForm):
    nombre = StringField(
        "Nombre de la Presentación",
        validators=[DataRequired(message="El nombre es obligatorio."), Length(max=100)],
    )
    tipo_medida_id = SelectField(
        "Tipo de Medida",
        coerce=int,
        validators=[DataRequired(message="Debe seleccionar un tipo de medida.")],
    )
    cantidad_equivalente = DecimalField(
        "Cantidad Equivalente",
        validators=[DataRequired(message="La cantidad es obligatoria.")],
    )
    medida = SelectField(
        "Medida",
        validators=[DataRequired(message="Debe seleccionar una medida.")],
    )
