from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from app.database import db

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