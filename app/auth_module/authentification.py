
from .models import Customer, PrevModelInput, db
from app.login_manager import lm
from flask import render_template, jsonify, request, redirect, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, logout_user

from email_validator import validate_email, EmailNotValidError

from datetime import datetime


module = Blueprint("main_module", __name__)

@module.route("/login", methods=["GET", "POST"])
def login():
    try:
        data = request.get_json(silent=True)
        if not data or "email" not in data.keys() or "pass" not in data.keys(): return render_template("login.html")
        if (data["email"] == "" or data["pass"] == ""): return jsonify(status="error", message="Заполните все данные")
        user = Customer.query.filter_by(email=data["email"]).first()
        if (not user): return jsonify(status="error", message="Неправильная почта или пароль")
        if (not check_password_hash(user.password, data["pass"])): return jsonify(status="error", message="Неправильная почта или пароль")
        login_user(user)
        return jsonify(status="ok", message="login completed")
    except Exception as ex:
        db.session.rollback()
        print(f"Login error: {ex}")
        return render_template("error.html")
    
@module.route("/registration", methods=["POST", "GET"])
def registration():
    try:
        data = request.get_json(silent=True)
        if not data or "email" not in data.keys() or "pass" not in data.keys(): return render_template("registration.html")
        if (data["email"] == "" or data["pass"] == ""): return jsonify(status="error", message="Заполните все данные")
        valid = validate_email(data['email'])
        if (Customer.query.filter_by(email=data["email"]).first()): return jsonify(status="error", message="Пользователь с такой почтой уже существует")
        user = Customer(email=data["email"], password=generate_password_hash(data["pass"], "bcrypt:sha256", salt_length=32), regDate=datetime.utcnow())
        db.session.add(user)
        db.session.commit()  
        login_user(user)
        return jsonify(status="ok", message="registration completed")
    except EmailNotValidError as ex:
        return jsonify(status="error", message="Неверный формат почты")
    except Exception as ex:
        db.session.rollback()
        print(f"Registration error: {ex}")
        return render_template("error.html")

@module.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for("home"))

@lm.user_loader
def load_user(user_id):
    return Customer.query.get(user_id)

def get_prev_model_inputs(email):
    prev_model_input = {}
    user = Customer.query.filter_by(email=email).first()
    if not user: return {}
    for record in user.prevModelData:
            prev_model_input[record.id] = {
                "input": record.modelInput,
                "record_date": record.regDate,
                "model_answer": record.modelAnswer
                }
    return prev_model_input