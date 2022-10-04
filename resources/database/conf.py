from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)
# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# api = Api(app)
# db = base.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()
