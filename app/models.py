import json, uuid
from app import db, login
import bcrypt
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    #email = db.Column(db.String(), nullable=False, default=secret.dump('nomail@all'))  # enc, updatable
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    settings = db.Column(db.String(), nullable=False, default='{}')  #updatable
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    last_modified_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    is_enabled = db.Column(db.Boolean, nullable=False, default=True)
    authenticated = db.Column(db.Boolean, nullable=False, default=False)
    expiration = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Username: {self.username}> <is superuser:{self.is_superuser}>'


    def set_password(self, password):
        salt = bcrypt.gensalt(14)
        p_bytes = password.encode()
        pw_hash = bcrypt.hashpw(p_bytes, salt)
        self.password_hash = pw_hash.decode()
        self.salt = salt.decode()
        return True


    def check_password(self, password):
        c_password = bcrypt.hashpw(password.encode(), self.salt.encode()).decode()
        if c_password == self.password_hash:
            return True
        else:
            return False


    def get_self(self):
        return json.dumps({'ID': self.id, 'username': self.username, 'APIkey': self.APIkey,
                           'created': self.created.strftime("%m/%d/%Y, %H:%M:%S"), 'is superuser': self.is_superuser})


    def get_self_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'settings': self.settings,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_modified_at': self.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'is_superuser': self.is_superuser,
            'is_enabled': self.is_enabled
        }


    def get_self_json_enc(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': str(secret.load(self.email)),
            'settings': self.settings,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_modified_at': self.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'is_superuser': self.is_superuser,
            'is_enabled': self.is_enabled
        }