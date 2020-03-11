import os
import sys
import logging

from flask import Flask
from flask_cors import CORS
from . import configs
sys.path.append(os.path.abspath("../../"))
from .controllers import api_blueprint


def create_app():

    app = Flask(__name__)
    app.config.from_object(configs.Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(api_blueprint)

    return app