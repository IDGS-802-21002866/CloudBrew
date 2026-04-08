from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class RecetaForm(FlaskForm):
    nombre = StringField(
        "Nombre de la Receta",
        validators=[DataRequired(message="El nombre es obligatorio."), Length(max=255)],
    )
    descripcion = StringField("Descripción", validators=[Optional(), Length(max=500)])
    cantidad_producida = DecimalField(
        "Cantidad Producida",
        validators=[DataRequired(message="La cantidad producida es obligatoria.")],
    )
    imagen = FileField(
        "Imagen",
        validators=[
            Optional(),
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"], "Solo imágenes (jpg, png, webp)."
            ),
        ],
    )
    submit = SubmitField("Guardar")


class RecetaDetalleForm(FlaskForm):
    materia_prima_id = SelectField(
        "Materia Prima",
        validators=[DataRequired(message="Debe seleccionar una materia prima.")],
    )
    cantidad = DecimalField(
        "Cantidad",
        validators=[DataRequired(message="La cantidad es obligatoria.")],
    )
    submit = SubmitField("Agregar")


class ProcesoRecetaForm(FlaskForm):
    proceso_productivo_id = SelectField(
        "Proceso Productivo",
        validators=[DataRequired(message="Debe seleccionar un proceso productivo.")],
    )
    tiempo_estimado = DecimalField(
        "Tiempo Estimado (minutos)",
        validators=[DataRequired(message="El tiempo estimado es obligatorio.")],
    )
    submit = SubmitField("Agregar")
