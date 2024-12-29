# ruff: noqa: E501
from .base import *  # noqa: F403, I001
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = ["*"]
