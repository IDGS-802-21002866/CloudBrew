from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Optional


class PedidoForm(FlaskForm):
    cliente_id = HiddenField("Cliente ID", validators=[DataRequired(message="Debe seleccionar un cliente.")])


class PedidoDetalleForm(FlaskForm):
    receta_id = SelectField("Receta", coerce=int, validators=[DataRequired(message="Debe seleccionar una receta.")])
    cantidad_lotes = IntegerField("Cantidad de Lotes", validators=[DataRequired(message="La cantidad de lotes es obligatoria.")])
