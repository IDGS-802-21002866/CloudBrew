from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class backup_form(FlaskForm):
    pass


class restore_form(FlaskForm):
    file = FileField(
        "Archivo de Restauración",
        validators=[
            DataRequired(message="El archivo es obligatorio."),
            FileAllowed(["sql"], "Solo archivos SQL."),
        ],
    )
