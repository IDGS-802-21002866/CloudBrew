from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, DateField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class ProduccionForm(FlaskForm):
    id_receta = SelectField(
        'Receta',
        coerce=int,
        validators=[DataRequired()]
    )
    fecha_inicio = DateField(
        'Fecha Inicio',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )

    fecha_fin = DateField(
        'Fecha Fin',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("pendiente", "Pendiente"),
            ("en_proceso", "En proceso"),
            ("completado", "Completado"),
            ("cancelado", "Cancelado"),
        ],
        validators=[DataRequired()]
    )
    cantidad = IntegerField(
        'Cantidad',
        default=1,
        validators=[DataRequired(), NumberRange(min=1,max=10)]
    )

class ProduccionProcesoForm(FlaskForm):
    id_proceso = SelectField(
        'Proceso Productivo',
        coerce=int,
        validators=[DataRequired()]
    )

    fecha_inicio = DateField(
        'Fecha Inicio',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )

    fecha_fin = DateField(
        'Fecha Fin',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("pendiente", "Pendiente"),
            ("en_proceso", "En proceso"),
            ("completado", "Completado"),
            ("cancelado", "Cancelado"),
        ],
        validators=[DataRequired()]
    )