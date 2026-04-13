from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, number_range


class MermaForm(FlaskForm):
    materia_prima_id = SelectField(
        "Materia Prima",
        coerce=int,
        validators=[DataRequired(message="Debe seleccionar una materia prima.")],
    )
    cantidad = DecimalField(
        "Cantidad",
        places=2,
        validators=[DataRequired(message="La cantidad es obligatoria."), number_range(min=0.01,max=1000 ,message="La cantidad debe ser mayor a cero y menor a mil.")],
        default=0.00,
    )
    motivo = TextAreaField(
        "Motivo",
        validators=[
            DataRequired(message="El motivo es obligatorio."),
            Length(max=255, message="El motivo no puede tener más de 255 caracteres."),
        ],
    )
    medida = SelectField(
        "Medida",
        validators=[DataRequired(message="Debe seleccionar una medida.")],
    )
