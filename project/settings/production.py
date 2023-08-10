from project.settings.base import *
import os

DEBUG = False
ALLOWED_HOSTS = [os.environ.get("FLY_DOMAIN"),]
CSRF_TRUSTED_ORIGINS = ["https://" + os.environ.get("FLY_DOMAIN"),]
SECRET_KEY = os.environ.get("SECRET_KEY")