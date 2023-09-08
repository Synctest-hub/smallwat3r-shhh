from collections import OrderedDict
from enum import Enum

READ_TRIES_VALUES = (3, 5, 10)
DEFAULT_READ_TRIES_VALUE = 5

EXPIRATION_TIME_VALUES = OrderedDict([
    ("10 minutes", "10m"), ("30 minutes", "30m"), ("An hour", "1h"),
    ("3 hours", "3h"), ("6 hours", "6h"), ("A day", "1d"), ("2 days", "2d"),
    ("3 days", "3d"), ("5 days", "5d"), ("A week", "7d")
])
DEFAULT_EXPIRATION_TIME_VALUE = EXPIRATION_TIME_VALUES["3 days"]


class ClientType(str, Enum):
    WEB = "web"
    TASK = "task"


class EnvConfig(str, Enum):
    TESTING = "testing"
    DEV_LOCAL = "dev-local"
    DEV_DOCKER = "dev-docker"
    HEROKU = "heroku"
    PRODUCTION = "production"