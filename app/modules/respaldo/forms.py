import os
from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField, FileAllowed, ValidationError
from wtforms.validators import DataRequired, Length, ValidationError


class backup_form(FlaskForm):
    route = StringField(
        "Ruta del Backup",
        validators=[
            DataRequired(message="La ruta es obligatoria."),
            Length(max=255, message="La ruta no debe exceder 255 caracteres."),
        ],
    )

    def validate_route(self, field):
        path = field.data.strip()
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise ValidationError("La ruta no existe.")
        if not os.path.isdir(path):
            raise ValidationError("La ruta debe ser una carpeta válida.")
        if not os.access(path, os.W_OK):
            raise ValidationError("No tienes permisos de escritura en esa ruta.")
        
class restore_form(FlaskForm):
     file = FileField(
        "Archivo de Restauración",
        validators=[
            DataRequired(message="El archivo es obligatorio."),
            FileAllowed(
                ["sql"], "Solo archivos SQL."
            ),
        ]
        )