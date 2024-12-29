from flask import Flask, render_template, request, redirect, flash,url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from app.forms import LoginForm
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db,login_manager
import json

bp = Blueprint("main",__name__)
# API
api_openai = "https://api.openai.com/v1/chat/completions"
api_key=os.getenv("API_KEY")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# model for users and animal table
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    animals = db.relationship("Animal")

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    life_expectation = db.Column(db.String(100), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@bp.route("/")
def index():
    animals = Animal.query.all()
    return render_template("index.html", animals=animals, user=current_user)

@bp.route("/add", methods=["POST"])
def add_animal():
    name = request.form["name"]
    life_exp = request.form["life_exp"]
    try:
        new_animal = Animal(name=name, life_expectation=life_exp, user_id=current_user.id)
        db.session.add(new_animal)
        db.session.commit()

    except Exception as e:
        print(e)
    return redirect(url_for("main.index"))

@bp.route("/get_info", methods=["POST"])
def get_info():
    input = request.form["userinput"]
    try:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an assistant that is supposed to give answers about animal data as short as possible"},
                {"role": "user", "content": "{}".format(input)}
            ],
        "temperature": 0.7
        }
        response = requests.post(api_openai, headers=headers, data=json.dumps(data))
        print(response.status_code)
        print(response.json())
        if response.status_code==200:
            result = response.json()

            chatgpt_response = result["choices"][0]["message"]["content"]
            return render_template("index.html", gptresponse=chatgpt_response, user=current_user)

    except Exception as e:
        print(e)

    return redirect(url_for("main.index"))

@bp.route("/del_animal", methods=["POST"])
def delete_animal():
    animal_id = request.form["del_animal"]
    try:
        animal = db.session.get(Animal,animal_id)
        if animal.user_id==current_user.id:
            db.session.delete(animal)
            db.session.commit()
    except Exception as e:
        print(e)

    return redirect(url_for("main.index"))

@bp.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    email = form.username.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()

    if form.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(
              form.username.data, form.remember_me.data))
        if user:
            if check_password_hash(user.password,password):
                flash("Login successful")
                login_user(user,remember=form.remember_me.data)
                return redirect(url_for("main.index"))
            else:
                flash("Incorrect password.")
        else:
            flash("Email doesn't exist.")
    return render_template("login.html", title="Sign In", form=form, user=current_user)

@bp.route("/signup", methods=["POST","GET"])
def signup():
    form=LoginForm()
    if request.method=="POST":
        email= form.username.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists")
        elif len(password)<4:
            flash("Password must be atleast 4 characters")
        else:
            user=User(email=email,name=email[:5],password=generate_password_hash(password,method="pbkdf2:sha256"))
            db.session.add(user)
            db.session.commit()
            login_user(user,remember=form.remember_me.data)
            return redirect(url_for("main.index"))
    return render_template("signup.html",form=form, user=current_user)


@bp.route("/logout")
def logout():
    try:
        logout_user()
    except Exception as e:
        print(e)
    return redirect(url_for("main.login"))





