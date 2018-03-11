from flask import Flask
import os

class ConfigClass(object):
    DEBUG = True

def register_models(app):
    from . import models

def register_blueprints(app):
    from .basic import app as basic_bp
    app.register_blueprint(basic_bp)

def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__ + '.ConfigClass')

    app.config['SECRET_KEY'] = b's\xb1!\x94M\xca\ry~\xcbl\x8d\xb9\xfaV\x11\xee\xc8\x00\xa0L@\xbf\x9c' if 'FLASK_SECRET_KEY' not in os.environ else os.environ['FLASK_SECRET_KEY'] 

    register_models(app)
    register_blueprints(app)

    return app
