from flask import Flask
from flask_login import LoginManager

from komradebank.models import db, User
from komradebank.controllers.main import main

import os, sys

login_manager = LoginManager()
login_manager.login_view = "main.login"


def create_app():

    # create / configure app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = b's\xb1!\x94M\xca\ry~\xcbl\x8d\xb9\xfaV\x11\xee\xc8\x00\xa0L@\xbf\x9c' if 'FLASK_SECRET_KEY' not in os.environ else os.environ['FLASK_SECRET_KEY']

    # init database, and populate if required
    createDB = len(sys.argv) > 1 and sys.argv[1] == '-drop'
    db.init_app(app, createDB)

    # init login manager
    login_manager.init_app(app)

    # add controllers
    app.register_blueprint(main)

    return app


@login_manager.user_loader
def load_user(id):
    return User.by_id(id)
