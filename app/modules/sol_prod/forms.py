from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField, DateField
from wtforms.validators import DataRequired

class PedidoForm(FlaskForm):
    id_cliente = SelectField(
        "Cliente",
        coerce=int,
        validators=[DataRequired()]
    )

    fecha_pedido = DateField(
        "Fecha",
        format="%Y-%m-%d",
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

class DetallePedidoForm(FlaskForm):
    id_receta = SelectField(
        "Receta",
        coerce=int,
        validators=[DataRequired()]
    )

    cantidad = FloatField(
        "Cantidad",
        validators=[DataRequired()]
    )

    submit = SubmitField("Agregar")

class PedidoProduccionForm(FlaskForm):
    id_pedido = SelectField(
        "Pedido",
        coerce=int,
        validators=[DataRequired()]
    )

    id_produccion = SelectField(
        "Producción",
        coerce=int,
        validators=[DataRequired()]
    )

    submit = SubmitField("Vincular")