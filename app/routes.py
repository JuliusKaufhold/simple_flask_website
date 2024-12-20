from app import app
from flask import Flask, render_template, request, redirect, flash,url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from app.forms import LoginForm

# API
api_random_user = "https://randomuser.me/api/"

#db init
db = SQLAlchemy(app)

# model for users table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# create table in database
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    users = User.query.all()  # Alle Benutzer aus der Datenbank abrufen
    return render_template("index.html", users=users)

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]

    # create new user
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/add_random", methods=["POST"])
def add_random_user():
    try:
        response = requests.get(api_random_user)

        if response.status_code==200:
            random_user = response.json()

            first_name = random_user["results"][0]["name"]["first"]
            last_name = random_user["results"][0]["name"]["last"]
            name = first_name + " " +  last_name
            email = name + "@randommail.com"

            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()

        return redirect("/")

    except Exception as e:
        print(e)

@app.route("/del_user", methods=["POST"])
def delete_user():
    user_id = request.form["del_user"]
    try:
        user = db.session.get(User,user_id)
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print(e)

    return redirect("/")

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(
              form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template("login.html", title="Sign In", form=form)



