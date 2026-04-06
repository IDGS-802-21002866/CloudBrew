from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Optional


class UnidadMedidaForm(FlaskForm):
    nombre = StringField(
        "Nombre de la Unidad",
        validators=[DataRequired(message="El nombre es obligatorio"), Length(max=50)],
    )
    abreviatura = StringField(
        "Abreviatura",
        validators=[
            DataRequired(message="La abreviatura es obligatoria"),
            Length(max=10),
        ],
    )
    tipo_medida_id = SelectField(
        "Tipo de Medida",
        coerce=int,
        validators=[DataRequired(message="Selecciona un tipo de medida")],
    )
    valor_conversion = DecimalField(
        "Valor de Conversión",
        validators=[DataRequired(message="El valor de conversión es obligatorio")],
    )
