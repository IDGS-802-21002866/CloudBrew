from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Length, Optional

class UnidadMedidaForm(FlaskForm):
    nombre = StringField(
        "Nombre de la Unidad", 
        validators=[DataRequired(message="El nombre es obligatorio"), Length(max=50)]
    )
    abreviatura = StringField(
        "Abreviatura", 
        validators=[DataRequired(message="La abreviatura es obligatoria"), Length(max=10)]
    )
    tipo = SelectField(
        "Tipo", 
        choices=[('Masa', 'Masa'), ('Volumen', 'Volumen'), ('Pieza', 'Pieza')],
        validators=[DataRequired(message="Selecciona un tipo")]
    )
    es_base = BooleanField("¿Es Unidad Base?")
    
    unidad_base = SelectField("Unidad Base de Referencia", coerce=int, validators=[Optional()])
    valor_conversion = DecimalField("Valor de conversión", validators=[Optional()])