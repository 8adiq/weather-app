from flask import Flask,jsonify,request
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
    
# Initializing SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Database configration and connection
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}:{os.getenv("port")}/{os.getenv("dbname")}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # binding the SQLAlchemy db to the flask app
    db.init_app(app)


    # importing routes  
    from routes import all_routes
    all_routes(app,db)

    # handling db migrations
    migrate = Migrate(app,db)

    return app

