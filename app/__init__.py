from flask import Flask
from .database import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///customers.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    with open("secret_key.txt") as file:
        app.config["SECRET_KEY"] = file.readline()
    app.config["SESSION_TYPE"] = "filesystem"

    db.init_app(app)
    with app.app_context():
        db.create_all()
    import app.auth_module.authentification as auth_module
    import app.general.routes as general_module
    
    app.register_blueprint(general_module.module)
    app.register_blueprint(auth_module.module)

    from .login_manager import lm
    lm.init_app(app)
    return app