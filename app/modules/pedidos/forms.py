from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Optional


class PedidoForm(FlaskForm):
    cliente_id = HiddenField(
        "Cliente ID", validators=[DataRequired(message="Debe seleccionar un cliente.")]
    )


class PedidoDetalleForm(FlaskForm):
    producto_venta_id = SelectField(
        "Producto",
        coerce=int,
        validators=[DataRequired(message="Debe seleccionar un producto.")],
    )
    cantidad = IntegerField(
        "Cantidad",
        validators=[DataRequired(message="La cantidad es obligatoria.")],
    )
