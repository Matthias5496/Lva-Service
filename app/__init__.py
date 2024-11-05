import os
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)
migrate = Migrate(app, db)

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')

from .routes import routes
from .auth import auth
app.register_blueprint(routes, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

from app import models

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')


# Rufe die Funktion auf, um die Datenbank zu erstellen
create_database(app)
