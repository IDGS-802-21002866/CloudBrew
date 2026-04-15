from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, HiddenField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class MermaProductoTerminadoForm(FlaskForm):
    producto_terminado = StringField(
        "Producto Terminado",
        validators=[DataRequired(message="Debe seleccionar un producto terminado activo.")],
    )
    receta_id = HiddenField()
    es_lote_completo = BooleanField("Es merma de lote completo")
    lote_id = HiddenField()
    cantidad = DecimalField(
        "Cantidad",
        places=2,
        validators=[
            DataRequired(message="La cantidad es obligatoria."),
            NumberRange(min=0.01, message="La cantidad debe ser mayor a cero."),
        ],
    )
    motivo = TextAreaField(
        "Motivo",
        validators=[
            DataRequired(message="El motivo es obligatorio."),
            Length(min=10, max=255, message="El motivo debe tener entre 10 y 255 caracteres."),
        ],
    )
