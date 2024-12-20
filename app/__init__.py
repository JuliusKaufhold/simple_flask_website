from flask import Flask
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

# connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:changeme@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

from app import routes
