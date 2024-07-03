from flask_login import login_required, current_user
from flask import render_template, jsonify, request, redirect, Blueprint, make_response
from app.auth_module.models import db, PrevModelInput
from app.predictive_model.predictive_model import model
from app.parsing.parsing import parse_text
from flask_caching import Cache, CachedResponse
from datetime import datetime
from requests.exceptions import InvalidURL
import json

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
            prev_input = get_html_model_answ()
            return render_template("user_page.html", records=prev_input)
        if (data["url"] == ""): return jsonify(status="error", message="Заполните все данные")
        inp = parse_text(data["url"])
        prediction = model.predict(inp).get_rate()
        prediction = format_prediction_data(prediction)
        model_inp = PrevModelInput(modelInput=data["url"], modelAnswer=str(prediction), modelText=inp, recordDate=datetime.utcnow(), userId=current_user.id)
        db.session.add(model_inp)
        db.session.commit()
        return CachedResponse(response=make_response(jsonify(status="ok", output=prediction)), timeout=10800)
    except InvalidURL:
        print("INVALID")
        return jsonify(status="error", message=f"Неверный формат ссылки")
    except Exception as ex:
        db.session.rollback()
        print(f"User page error: {ex}")
        return jsonify(status="error", message=f"Запрос не выполнен. Повторите попытку позже")

@module.route("/guest", methods=["GET", "POST"])
def guest_page():
    try:
        data = request.get_json(silent=True)
        if not data or "url" not in data.keys():
            return render_template("guest_page.html")
        if (data["url"] == ""): return jsonify(status="error", message="Заполните все данные")
        inp = parse_text(data["url"])
        prediction = model.predict(inp).get_rate()
        prediction = format_prediction_data(prediction)
        return CachedResponse(response=make_response(jsonify(status="ok", output=prediction)), timeout=10800)
    except InvalidURL:
        return jsonify(status="error", message=f"Неверный формат ссылки")
    except Exception as ex:
        db.session.rollback()
        print(f"Guest page error: {ex}")
        return jsonify(status="error", message=f"Запрос не выполнен. Повторите попытку позже")

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

def format_prediction_data(pred_rates):
    out = {"companies": []}
    for cmp in pred_rates.keys():
        if pred_rates[cmp] >= 0.3:
            out["companies"].append(
                {
                    "name": cmp,
                    "estimate": "POSITIVE"
                }
            )
        elif pred_rates[cmp] <= -0.3:
            out["companies"].append(
                {
                    "name": cmp,
                    "estimate": "NEGATIVE"
                }
            )
        else:
            out["companies"].append(
                {
                    "name": cmp,
                    "estimate": "NEUTRAL"
                }
            )
    return out

def get_html_model_answ():
    out = ""
    for record in current_user.prevModelData:
        out += f"<tr>" \
            f"<th scope='row'>{record.recordDate}</th>" \
            f"<th scope='row'>{record.modelInput}</th>" \
            f"<th scope='row'>{record.modelText[:20]}</th>" \
            "<th scope='row'>" 
        ans = record.modelAnswer.replace("'", '"')
        cmps = json.loads(ans)["companies"]
        for cmp in cmps:
            out += f"{cmp['name']}: {cmp['estimate']}; "
        out += "</th></tr>"
    return out


