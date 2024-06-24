from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__, template_folder="static")

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
        return jsonify(status="ok")
    except Exception as ex:
        print(f"Registration error: {ex}")
        return jsonify(status="error", message="Неизвестная ошибка")

if __name__ == "__main__":
    app.run(debug=True)