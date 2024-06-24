from flask import Flask, render_template, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

app = Flask(__name__, template_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///customers.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/")
def debug():
    return render_template("index.html")

@app.route("/get")
def get_smth():
    return jsonify(status="ok", data={"status": "ok"})
    
@app.route("/registration", methods=["POST"])
def registration():
    try:
        data = dict(json.loads(request.data.decode("utf-8")))
        print(data, type(data), data['name'])
        if (data["action"] != "registration"): return jsonify(status="error", message="wrong action")
        if (data["email"] == "" or data["pass"] == ""): return jsonify(status="error", message="empty data")

        return jsonify(status="ok")
    except Exception as ex:
        print(f"Registration error: {ex}")
        return jsonify(status="error", message="Неизвестная ошибка")

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    regDate = db.Column(db.DateTime, default=datetime.now(datetime.UTC))
    prevModelData = db.relationship("customer", backref = 'PrevModelData', lazy=True)

class PrevModelInput(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    modelInput = db.Column(db.text, default="")
    recordDate = db.Column(db.DateTime, default=datetime.now(datetime.UTC))

if __name__ == "__main__":
    app.run(debug=True)