import os
import sys
import logging

from flask import Flask
from flask_cors import CORS

sys.path.append(os.path.abspath("../../"))
from . import configs
from .controllers import api_blueprint


def create_app():

    app = Flask(__name__)
    app.config.from_object(configs.Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(api_blueprint)
    logging.basicConfig(
        format="[%(asctime)s] [%(process)d] [%(levelname)s] %(filename)s - %(funcName)s: %(message)s"
    )

    return app
