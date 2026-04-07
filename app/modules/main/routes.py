from flask import render_template
from app.modules.main import bp


@bp.route("/", methods=["GET"])
def index():
    return render_template("main/index.html")


@bp.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("main/dashboard.html")
