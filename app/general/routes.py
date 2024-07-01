from flask_login import login_required, current_user
from flask import render_template, jsonify, request, redirect, url_for, Blueprint
from app.auth_module.models import db
from app.predictive_model.predictive_model import model
from app.parsing.parsing import parse_text
from flask_caching import Cache, CachedResponse

module = Blueprint("general", __name__)
cache = Cache()

@module.route("/", methods=["POST", "GET"])
def home():
    return render_template("index.html")

@module.route("/user", methods=["GET", "POST"])
@login_required
@cache.cached()
def user_page():
    try:
        data = request.get_json(silent=True)
        print(data)
        if not data or "url" not in data.keys():
            prev_input = get_prev_model_inputs()
            print(prev_input)
            return render_template("model.html", records=prev_input)
        if (data["url"] == ""): return jsonify(status="error", message="Заполните все данные")
        inp = parse_text(data["url"])
        return CachedResponse(response=jsonify(status="ok", output=f"{model.predict(inp)}"), timeout=10800)
    except Exception as ex:
        db.session.rollback()
        print(f"Login error: {ex}")
        return jsonify(status="error", message=f"Неверный формат ссылки")

@module.route("/error", methods=["GET"])
def error_page():
    return render_template("error.html")

def get_prev_model_inputs():
    prev_model_input = []
    if not current_user.is_authenticated : return {}
    for record in current_user.prevModelData:
            prev_model_input.append({
                "input": record.modelInput,
                "text": record.modelText,
                "record_date": record.recordDate,
                "model_answer": record.modelAnswer
                })
    return prev_model_input