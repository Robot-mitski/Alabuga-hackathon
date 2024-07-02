from flask_login import login_required, current_user
from flask import render_template, jsonify, request, redirect, url_for, Blueprint, make_response
from app.auth_module.models import db
from app.predictive_model.predictive_model import model
from app.parsing.parsing import parse_text
from flask_caching import Cache, CachedResponse

module = Blueprint("general", __name__)
cache = Cache()

@module.route("/", methods=["POST", "GET"])
def home():
    return redirect("/registration")

@module.route("/user", methods=["GET", "POST"])
@login_required
def user_page():
    try:
        data = request.get_json(silent=True)
        print(data)
        if not data or "url" not in data.keys():
            prev_input = get_prev_model_inputs()
            print(prev_input)
            return render_template("user_page.html", records=prev_input)
        if (data["url"] == ""): return jsonify(status="error", message="Заполните все данные")
        inp = parse_text(data["url"])
        return CachedResponse(response=jsonify(status="ok", output=f"{model.predict(inp)}"), timeout=10800)
    except Exception as ex:
        db.session.rollback()
        print(f"Login error: {ex}")
        return jsonify(status="error", message=f"Неверный формат ссылки")

@module.route("/guest", methods=["GET", "POST"])
def guest_page():
    # try:
        data = request.get_json(silent=True)
        if not data or "url" not in data.keys():
            return render_template("guest_page.html")
        if (data["url"] == ""): return jsonify(status="error", message="Заполните все данные")
        inp = parse_text(data["url"])
        prediction = model.predict(inp).get_labels()
        return CachedResponse(response=make_response(jsonify(status="ok", output=prediction)), timeout=10800)
    # except Exception as ex:
    #     db.session.rollback()
    #     print(f"Login error: {ex}")
    #     return jsonify(status="error", message=f"Неверный формат ссылки")

@module.route("/error", methods=["GET"])
def error_page():
    return render_template("error.html")

@module.after_request
def after_req(response):
    if response.status_code == 401:
        return redirect("/guest")
    return response

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

