from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id =  db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

class Contest1Sub(db.Model):
    __tablename__ = "Contest1Sub"
    id =  db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    answers = db.Column(db.String, nullable=False)
