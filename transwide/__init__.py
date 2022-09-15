from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_pymongo import PyMongo

db = SQLAlchemy()
mail = Mail()
mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    ENV = 'dev'

    if ENV == 'dev':

        app.debug = True
        app.config['SECRET_KEY'] = 'thisisdasecretkey'
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/transwide"

    else:
        app.debug = False
        app.config['SECRET_KEY'] = 'thisisdasecretkey'
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/transwide"


    db.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app