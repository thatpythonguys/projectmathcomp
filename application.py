import os
import requests
import eventlet
eventlet.monkey_patch()
from flask import Flask, session, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from collections import deque
from models import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

def main():
    db.create_all()

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/contests")
def contests():
    return render_template("contests.html")

@app.route("/confirmation/<contestnumber>", methods = ["GET","POST"])
def confirm(contestnumber):
    if "logged_in" not in session or session.get("logged_in") == False:
        return redirect('/login')
    return render_template("contestconfirmationpage.html", contestnumber=contestnumber)

@app.route("/contest/<contestnumber>", methods = ["POST"])
def contest(contestnumber):
    if "logged_in" not in session or session.get("logged_in") == False:
        return redirect('/login')
    return render_template("individualcontest.html")
@app.route("/answersuccess", methods = ["POST"])
def answersuccess():
    answers = []
    try:
        answers.append(request.form.getlist('q1')[0])
    except:
        answers.append("noans")
    try:
        answers.append(request.form.getlist('q2')[0])
    except:
        answers.append("noans")
    try:
        answers.append(request.form.getlist('q3')[0])
    except:
        answers.append("noans")
    try:
        answers.append(request.form.getlist('q4')[0])
    except:
        answers.append("noans")
    try:
        answers.append(request.form.getlist('q5')[0])
    except:
        answers.append("noans")
    try:
        answers.append(request.form.getlist('q6')[0])
    except:
        answers.append("noans")
    try:
        answers.append(request.form.getlist('q7')[0])
    except:
        answers.append("noans")
    try:
        answers.append(request.form.getlist('q8')[0])
    except:
        answers.append("noans")
    try:
        answers.append(request.form.getlist('q9')[0])
    except:
        answers.append("noans")
    try:
        answers.append(request.form.getlist('q10')[0])
    except:
        answers.append("noans")
    answers.append(request.form.get('q11'))
    answers.append(request.form.get('q12'))
    answers.append(request.form.get('q13'))
    answers.append(request.form.get('q14'))
    answers.append(request.form.get('q15'))
    if "username" in session:
        username = session["username"]
    submission = Contest1Sub(username=username, answers=answers)
    db.session.add(submission)
    db.session.commit()

    return render_template("answersuccess.html", title="Well Done!")

@app.route("/guides")
def guides():
    return render_template("guides.html")

@app.route("/write")
def write():
    return render_template("write.html")

@app.route("/forums")
def forums():
    return render_template("forums.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("login.html", message="You forgot to type something.")
        u = Users.query.filter_by(username=username).first()
        if u.password == password:
            session["username"] = username
            session["logged_in"] = True
            return redirect('/')
        return render_template("login.html", message="Invalid Credentials.")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        if not username or not password or not email:
            return render_template("error.html", title="error", message="You forgot to enter some information.")
        user = Users(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return render_template("error.html", title="success", message="You have successfully created an Account!")
    if "username" in session:
        return redirect("/")
    return render_template("signup.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
