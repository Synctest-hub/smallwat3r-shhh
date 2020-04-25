import logging
from os import path

from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from kombu_fernet.serializers.json import MIMETYPE

db = SQLAlchemy()


def create_app(env):
    app = Flask(__name__)

    configurations = {
        "dev-local": "shhh.config.DefaultConfig",
        "dev-docker": "shhh.config.DockerConfig",
        "production": "shhh.config.ProductionConfig",
    }
    app.config.from_object(
        configurations.get(env, "shhh.config.ProductionConfig"))

    db.init_app(app)

    with app.app_context():
        celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
        celery.conf.update(CELERY_TASK_SERIALIZER="fernet_json",
                           CELERY_ACCEPT_CONTENT=[MIMETYPE])

        logging.basicConfig(
            level=logging.INFO,
            format=("[%(asctime)s] [sev %(levelno)s] [%(levelname)s] "
                    "[%(name)s]> %(message)s"),
            datefmt="%a, %d %b %Y %H:%M:%S")

        logging.getLogger("werkzeug").setLevel(logging.WARNING)
        logger = logging.getLogger("shhh")

        from .api import api
        app.register_blueprint(api)

        from . import views

        db.create_all()
        return app
