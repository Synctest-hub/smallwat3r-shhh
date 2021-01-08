import os
from typing import Optional

from shhh.scheduler import delete_expired_links


class DefaultConfig:
    """Default config values (dev-local)."""

    DEBUG = True
    FORCE_HTTPS = False

    # Scheduled jobs. Delete expired database records every 60 seconds.
    JOBS = [
        {
            "id": "delete_expired_links",
            "func": delete_expired_links,
            "trigger": "interval",
            "seconds": 60,
        }
    ]

    # Postgres connection.
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "shhh")

    # SqlAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI: Optional[str] = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # This variable can be used to specify a custom hostname to use as the
    # domain URL when Shhh creates a secret (ex: https://mydomain.com). If not
    # set, the hostname defaults to request.url_root, which should be fine in
    # most cases.
    SHHH_HOST = os.environ.get("SHHH_HOST")


class TestConfig(DefaultConfig):
    """Testing configuration."""

    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        f"{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db')}"
    )
    SHHH_HOST = "http://test.test"


class DockerConfig(DefaultConfig):
    """Docker development configuration (dev-docker)."""

    SQLALCHEMY_ECHO = False


class HerokuConfig(DefaultConfig):
    """Heroku configuration (heroku)."""

    DEBUG = False
    FORCE_HTTPS = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class ProductionConfig(DefaultConfig):
    """Production configuration (production)."""

    DEBUG = False
    FORCE_HTTPS = True
    SQLALCHEMY_ECHO = False
