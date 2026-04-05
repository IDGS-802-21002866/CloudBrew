from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length

class PresentacionForm(FlaskForm):
    nombre = StringField(
        "Nombre de la Presentación",
        validators=[DataRequired(message="El nombre es obligatorio."), Length(max=100)]
    )
    id_unidad = SelectField(
        "Unidad Base",
        coerce=int,
        validators=[DataRequired(message="Debe seleccionar una unidad base.")]
    )
    cantidad_equivalente = DecimalField(
        "Cantidad Equivalente",
        validators=[DataRequired(message="La equivalencia es obligatoria.")]
    )
