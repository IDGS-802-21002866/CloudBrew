from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange


class OrdenDeCompraForm(FlaskForm):
    proveedor_id = SelectField(
        "Proveedor",
        coerce=int,
        validators=[DataRequired(message="Debe seleccionar un proveedor.")],
    )


class OrdenDeCompraDetallesForm(FlaskForm):
    materia_prima_id = SelectField(
        "Materia Prima",
        validators=[DataRequired(message="Debes elegir una materia prima.")],
    )
    presentacion_id = SelectField(
        "Presentación",
        validators=[DataRequired(message="Debes elegir una presentación.")],
    )
    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(message="La cantidad es requerida."),
            NumberRange(min=1, message="La cantidad debe ser mayor a 0."),
        ],
    )


class OrdenDeCompraConfirmacionForm(FlaskForm):
    pass
