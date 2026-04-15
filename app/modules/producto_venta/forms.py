from decimal import Decimal

from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProductoVentaForm(FlaskForm):
    receta_id = SelectField("Receta", coerce=int, validators=[DataRequired()])
    presentacion_id = SelectField(
        "Presentación", coerce=int, validators=[DataRequired()]
    )
    nombre = StringField(
        "Nombre",
        validators=[DataRequired(message="El nombre es obligatorio."), Length(max=255)],
    )
    descripcion = TextAreaField("Descripción", validators=[Optional(), Length(max=500)])
    tipo = SelectField(
        "Tipo",
        choices=[("web", "Web"), ("retail", "Retail")],
        validators=[DataRequired()],
    )
    precio_venta = DecimalField(
        "Precio de Venta",
        validators=[
            DataRequired(message="El precio de venta es obligatorio."),
            NumberRange(min=0.01, message="El precio debe ser mayor a 0."),
        ],
        places=2,
    )
    submit = SubmitField("Guardar")
