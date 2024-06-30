from flask_login import login_required, current_user
from flask import render_template, jsonify, request, redirect, url_for, Blueprint
from app.auth_module.models import db
from app.predictive_model.predictive_model import model

module = Blueprint("general", __name__)

@module.route("/", methods=["POST", "GET"])
def home():
    return render_template("index.html")

@module.route("/user", methods=["GET", "POST"])
@login_required
def user_page():
    try:
        print(current_user.email)
        data = request.get_json(silent=True)
        if not data or "url" not in data.keys(): 
            print(data)
            return render_template("model.html")
        if (data["url"] == ""): return jsonify(status="error", message="Заполните все данные")
        inp = [list(map(float, data["url"].split()))]
        return jsonify(status="ok", output=f"{model.predict(inp)}")
    except Exception as ex:
        db.session.rollback()
        print(f"Login error: {ex}")
        return render_template("error.html")

@module.route("/error", methods=["GET"])
def error_page():
    return render_template("error.html")