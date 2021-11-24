from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_restful import Api


app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)


migrate = Migrate(app, db)


login = LoginManager(app)


api = Api(app)


from app import routes, models, workers, endpoints