import os
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate
#from flask_oidc import OpenIDConnect


db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)
migrate = Migrate(app, db)

# Keycloak OIDC-Konfiguration
app.config.update({
    'SESSION_TYPE': 'filesystem',
    #'SECRET_KEY': 'you_will_never_guess',
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    #'OIDC_ID_TOKEN_COOKIE_SECURE': False  # Für lokale Tests http statt https erlauben
})


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
