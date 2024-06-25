from app import app, db

with app.app_context() as ctx:
    db.create_all()