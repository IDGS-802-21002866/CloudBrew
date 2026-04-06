from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, Optional


class ProcesoProductivoForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            Optional(),
            Length(max=200)
        ]
    )

    submit = SubmitField("Guardar")