from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder="static")

@app.route("/")
def debug():
    return render_template("index.html")

@app.route("/get")
def get_smth():
    return jsonify(status="ok", data={"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)