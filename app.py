from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, UserMixin, AnonymousUserMixin, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import event
import joblib

app = Flask(__name__, template_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///customers.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
with open("secret_key.txt") as file:
    app.config["SECRET_KEY"] = file.readline()
app.config["SESSION_TYPE"] = "filesystem"
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

model = joblib.load("model/model.pkl")

with app.app_context():
    @event.listens_for(db.engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("index.html")

@app.route("/user", methods=["GET", "POST"])
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

@app.route("/login", methods=["GET", "POST"])
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
    
@app.route("/registration", methods=["POST", "GET"])
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
    
@app.route("/error", methods=["GET"])
def error_page():
    return render_template("error.html")

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

@app.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for("home"))

@lm.user_loader
def load_user(user_id):
    return Customer.query.get(user_id)

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    regDate = db.Column(db.DateTime)
    prevModelData = db.relationship("PrevModelInput", backref='customer')

class PrevModelInput(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    modelInput = db.Column(db.String(1024), default="")
    modelAnswer = db.Column(db.String(1024), default="")
    recordDate = db.Column(db.DateTime)
    userId = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete="CASCADE"))

class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'

if __name__ == "__main__":
    app.run(debug=True)
    