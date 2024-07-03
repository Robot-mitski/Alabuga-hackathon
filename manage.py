from app import create_app
from flask import redirect


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)