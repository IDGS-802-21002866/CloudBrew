from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, FloatField
from wtforms.validators import DataRequired, Optional, NumberRange, Length

class LoteProduccionForm(FlaskForm):
    id_produccion = IntegerField(
        'ID Producción',
        validators=[DataRequired(), NumberRange(min=1)]
    )

    codigo_lote = StringField(
        'Código de Lote',
        validators=[DataRequired(), Length(min=1, max=100)]
    )

    fecha_produccion = DateField(
        'Fecha de Producción',
        format='%Y-%m-%d',
        validators=[Optional()]
    )

    cantidad_generada = FloatField(
        'Cantidad Generada',
        validators=[Optional(), NumberRange(min=0)]
    )