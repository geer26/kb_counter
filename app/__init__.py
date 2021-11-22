from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from fernet import Secret

from cryptography.fernet import Fernet

import base64

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)

secret = Secret(app)

for i in range(10):
    print(Fernet.generate_key().decode())

from app import routes, models