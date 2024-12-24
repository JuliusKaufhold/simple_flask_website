from flask import Flask
from config import Config
import os

app = Flask(__name__)

app.config.from_object(Config)
password = os.getenv("DB_PW")
# connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/flask_db'.format(password)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

from app import routes
