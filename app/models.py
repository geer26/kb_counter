import json, uuid
from app import db, login, secret
import bcrypt
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(), nullable=False, default=secret.dump('nomail@all'))  # enc, updatable
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    #-------- Connections
    events = db.relationship('Event', backref='referee', lazy='dynamic', cascade="all, delete-orphan")
    workouts = db.relationship('Workout', backref='owner', lazy='dynamic', cascade="all, delete-orphan")


    def __repr__(self):
        return f'<Username: {self.username}> <ID:{self.id}>'


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


class Event(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    ident = db.Column(db.String(6), nullable=False)

    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    # -------- Connections
    competitors = db.relationship('Competitor', backref='event', lazy='dynamic', cascade="all, delete-orphan")


    def __init__(self):
        self.ident = self.gen_ident()


    def __repr__(self):
        return {'id':self.id, 'ident': self.ident, 'user': self.user}


    def gen_ident(self):
        uid = str(uuid.uuid1()).split('-')[3]
        ts = str(datetime.now().timestamp()).encode()
        ts_hash= bcrypt.hashpw(ts, bcrypt.gensalt()).decode()[51:53]
        return str(uid + ts_hash)


class Bell(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    value = db.Column(db.Integer, nullable=False, default=8)


    def __repr__(self):
        return {'value':self.value}


class Workout(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    wname = db.Column(db.String(64), unique=True, nullable=False)
    workout = db.Column(db.String(), default=None)
    '''
    eg.
    [{'max': 600(time in secs), 'type': 'warmup'(warmup/time/rest), 'add': 'KÉSZÜLJ!(plain text)'},{...}]
    '''
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)

    user = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return {'id':self.id, 'user': self.user, 'workout': self.workout}



class Competitor(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    wname = db.Column(db.String(64), unique=True, nullable=False)

    event = db.Column(db.Integer, db.ForeignKey('event.id'))
