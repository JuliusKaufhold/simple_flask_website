from app import app
from flask import Flask, render_template, request, redirect, flash,url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from app.forms import LoginForm
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash

# API
api_random_user = "https://randomuser.me/api/"

#db init
db = SQLAlchemy(app)

#login init
login_manager = LoginManager()
login_manager.login_view = "app.login"
login_manager.init_app(app)

# model for users table
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    animals = db.relationship("Animal")

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    life_expectation = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

# create table in database
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
def index():
    users = User.query.all()  # Alle Benutzer aus der Datenbank abrufen
    return render_template("index.html", users=users)

@app.route("/add", methods=["POST"])
@login_required
def add_animal():
    name = request.form["name"]
    life_exp = request.form["life_exp"]
    # create new user
    try:
        new_animal = Animal(name=name, life_expectation=life_exp, user_id=current_user.id)
        db.session.add(new_animal)
        db.session.commit()

    except Exception as e:
        print(e)
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
            password = "changeme"

            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for("index"))

    except Exception as e:
        print(e)

@app.route("/del_user", methods=["POST"])
@login_required
def delete_animal():
    animal_id = request.form["del_user"]
    try:
        user = db.session.get(Animal,animal_id)
        db.session.delete(animal)
        db.session.commit()
    except Exception as e:
        print(e)

    return redirect("/")

@app.route("/login", methods=["GET","POST"])
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
                return redirect(url_for("index"))
            else:
                flash("Incorrect password.")
        else:
            flash("Email doesn't exist.")
    return render_template("login.html", title="Sign In", form=form, user=current_user)

@app.route("/signup", methods=["POST","GET"])
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
            return redirect(url_for("index"))
    return render_template("signup.html",form=form, user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))





