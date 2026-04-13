from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, ValidationError
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, NumberRange


class RecetaForm(FlaskForm):
    def file_size_limit(max_size):
        def _file_size(form, field):
            if field.data:
                field.data.stream.seek(0, 2)
                size = field.data.stream.tell()
                field.data.stream.seek(0)


            if size > max_size:
                raise ValidationError(
                    f"La imagen excede el tamaño máximo de {max_size // 1024} KB."
                )
        return _file_size
    nombre = StringField(
        "Nombre de la Receta",
        validators=[DataRequired(message="El nombre es obligatorio."), Length(max=255)],
    )
    descripcion = StringField("Descripción", validators=[Optional(), Length(max=500)])
    cantidad_producida = DecimalField(
        "Cantidad Producida (botellas de 500ml)",
        validators=[DataRequired(message="La cantidad producida es obligatoria.")],
    )
    precio_venta = DecimalField(
        "Precio de Venta (por unidad)",
        validators=[
            Optional(),
            NumberRange(min=0.01, message="El precio debe ser mayor a 0."),
        ],
        places=2,
    )
    imagen = FileField(
        "Imagen",
        validators=[
            Optional(),
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"], "Solo imágenes (jpg, png, webp)."
            ),
            file_size_limit(64 * 1024)
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
        validators=[DataRequired(message="La cantidad es obligatoria."),NumberRange(min=0.01,max=100, message="La cantidad debe ser mayor a 0 y menor a 100.")],
        default=0.1
    )
    medida = SelectField(
        "Medida",
        validators=[DataRequired(message="Debe seleccionar una medida.")],
    )
    submit = SubmitField("Agregar")


class ProcesoRecetaForm(FlaskForm):
    proceso_productivo_id = SelectField(
        "Proceso Productivo",
        validators=[DataRequired(message="Debe seleccionar un proceso productivo.")],
    )
    tiempo_estimado = DecimalField(
        "Tiempo Estimado (minutos)",
        validators=[DataRequired(message="El tiempo estimado es obligatorio."), NumberRange(min=0.1, max=43800, message="El tiempo debe ser mayor a 0 y menor a 43800 (30 días) minutos.")],
    )
    submit = SubmitField("Agregar")
