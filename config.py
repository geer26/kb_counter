import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):

    # ----------SECRETS & COOKIES
    SECRET_KEY = os.environ.get('SECRET_KEY') or '01!ChAnGeThIs!10'
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME') or 'Fallback_cookie_name'
    COOKIE_LIFESPAN = os.environ.get('SESSION_LIFESPAN') or 60 * 60 * 24 * 30
    ENV_FOLDER = os.environ.get('KEY_FOLDER') or basedir

    # ----------STATICS & TEMPLATES
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # ----------LOGS
    LOG_FOLDER = os.path.join(basedir, 'log')

    # ----------DATABASE

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False