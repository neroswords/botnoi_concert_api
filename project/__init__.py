from flask import Flask, session, redirect, url_for
from functools import wraps
import json
from .extension import mongo
from .main import main
from flask_login import LoginManager, UserMixin
from .concert import concert
from .api import api

UPLOAD_FOLDER = './project/static/image'

def create_app(config_object='project.setting'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.secret_key = 'mysecret'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['DOWNLOAD_FOLDER'] = './static'
    mongo.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(api,url_prefix="/api")
    app.register_blueprint(concert,url_prefix="/concert")
    return app
