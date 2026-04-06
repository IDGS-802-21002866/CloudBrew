from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField
from wtforms.validators import DataRequired, Optional, Length


class MateriaPrimaForm(FlaskForm):
    nombre = StringField(
        "Nombre de la Materia Prima",
        validators=[DataRequired(message="El nombre es obligatorio."), Length(max=100)],
    )
    descripcion = StringField("Descripción", validators=[Optional(), Length(max=255)])
    tipo_medida_id = SelectField(
        "Tipo de Medida",
        coerce=int,
        validators=[DataRequired(message="Debe seleccionar un tipo de medida.")],
    )
    stock_minimo = DecimalField(
        "Stock Mínimo",
        validators=[DataRequired(message="El stock mínimo es obligatorio.")],
    )
