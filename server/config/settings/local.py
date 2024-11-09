# ruff: noqa: E501
from .base import *  # noqa: F403, I001
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="vSCRXILSCnOs973YzfHwur6gNxQY5xE6HPBNxZNOaJ6xC0YVysEgfMpu0HBgh8gt",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
