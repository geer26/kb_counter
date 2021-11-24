from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

from cryptography.fernet import Fernet

import base64, uuid
import bcrypt
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)

'''
for i in range(10):
    #print(Fernet.generate_key().decode())
    #print(str(datetime.now().timestamp())[-6:])
    uid = str(uuid.uuid1()).split('-')[3]
    ts = str(datetime.now().timestamp()).encode()
    ts_hash = bcrypt.hashpw(ts, bcrypt.gensalt()).decode()[51:53]
    print(uid+ts_hash)
'''

from app import routes, models