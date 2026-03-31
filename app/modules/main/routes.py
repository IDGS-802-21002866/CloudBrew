from flask import render_template
from flask_login import login_required

from app.modules.main import bp


@bp.route("/", methods=["GET"])
@login_required
def index():
    """Home page - requires login"""
    return render_template("main/index.html")


@bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """Dashboard - requires login"""
    return render_template("main/dashboard.html")
