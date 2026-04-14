from flask import (
    current_app,
    flash,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
import os
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask_login import login_required
from app.modules.respaldo.forms import backup_form, restore_form
from app.modules.respaldo.repository import restore_db
from app.modules.respaldo.service import RespaldoService
from . import bp

service = RespaldoService()


@login_required
@bp.route("/")
def index():
    form_backup = backup_form()
    form_restore = restore_form()
    return render_template(
        "respaldar.html", form_backup=form_backup, form_restore=form_restore
    )


@login_required
@bp.route("/respaldar", methods=["POST"])
def realizar_backup():
    import tempfile

    try:
        tmp_dir = tempfile.mkdtemp()
        filepath = service.crear_backup(tmp_dir)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("backup.index"))


@bp.route("/restaurar", methods=["POST"])
@login_required
def restore():
    form_restore = restore_form()
    if form_restore.validate_on_submit():
        file = form_restore.file.data
        upload_dir = os.path.join(current_app.root_path, "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_dir, filename)
        try:
            file.save(filepath)
            restore_db(filepath)
            flash("Backup restaurado correctamente", "success")

        except Exception as e:
            flash(f"Error al restaurar: {str(e)}", "error")

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    return redirect(url_for("backup.index"))
