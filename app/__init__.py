from flask import Flask
from config import Config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)
    password = os.getenv("DB_PW")
# connect to Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/flask_db'.format(password)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    db.init_app(app)
    login_manager.login_view = "app.login"
    login_manager.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)
    return app
