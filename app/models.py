import json, uuid
from app import db, login
import bcrypt
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    #email = db.Column(db.String(), nullable=False, default='nomail@all')
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)

    # -------- Connections
    # -------- BACKREF
    #events = db.relationship('Event', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    #workouts = db.relationship('Workout', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    #exercises = db.relationship('Exercise', backref='owner', lazy='dynamic', cascade="all, delete-orphan")


    def __repr__(self):
        return {'Username': self.username, 'ID':self.id}


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


    def get_self_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'is_superuser': self.is_superuser
        }


class Event(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    ident = db.Column(db.String(6), nullable=False)

    # -------- Connections
    # -------- FK
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    # -------- BACKREF
    #competitors = db.relationship('Competitor', backref='event', lazy='dynamic', cascade="all, delete-orphan")


    def __init__(self):
        self.ident = self.gen_ident()


    def __repr__(self):
        return {'id':self.id, 'ident': self.ident, 'user': self.user}


    def gen_ident(self):
        uid = str(uuid.uuid1()).split('-')[3]
        ts = str(datetime.now().timestamp()).encode()
        ts_hash= bcrypt.hashpw(ts, bcrypt.gensalt()).decode()[51:53]
        return str(uid + ts_hash)


    def get_ident(self):
        return str(self.ident)


class Workout(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    wname = db.Column(db.String(64), unique=True, nullable=False)
    workout = db.Column(db.String(), default=None)
    '''
    
    eg.
    [{'time': 600(time in secs), 'type': 'warmup'(warmup/time/rest), 'max': 120(maximum reps) , 'add': 'KÉSZÜLJ!(plain text)'},{...}]
    eg. pentathlon:
    [
    { 'time': 5, 'type': 'warmup', 'max': 0, 'add': 'Felkészülés'},
    { 'time': 360, 'type': 'time', 'max': 120, 'add': 'Clean'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'time', 'max': 60, 'add': 'Clean&Press'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'rest', 'max': 120, 'add': 'Jerk'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'rest', 'max': 108, 'add': 'Half Snatch'},
    { 'time': 300, 'type': 'rest', 'max': 0, 'add': 'Pihenő'},
    { 'time': 360, 'type': 'rest', 'max': 120, 'add': 'Push Press'}
    ]
    '''
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)

    # -------- Connections
    # -------- FK
    user = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return {'id':self.id, 'user': self.user, 'workout': self.workout}


    def get_workout(self):
        return json.dumps(self.workout)


class Competitor(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    cname = db.Column(db.String(64))
    association = db.Column(db.String(128))
    weight = db.Column(db.Integer, default=0)
    y_o_b = db.Column(db.Integer, default=1950)
    gender = db.Column(db.Integer, nullable=False, default=1)  # 1 - male, 2 - female
    result = db.Column(db.Integer, default=0)

    # -------- Connections
    # -------- FK

    event = db.Column(db.Integer, db.ForeignKey('event.id'))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))


    def __repr__(self):
        return {'id': self.id, 'name': self.name, 'result': self.result}


class Category(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(32))
    gender = db.Column(db.Integer, nullable=False, default=1)  # 1 - male, 2 - female
    level = db.Column(db.Integer, nullable=False, default=1)  # 1 - Amateur, 2- Intermediate
    age_min = db.Column(db.Integer, nullable=False, default=0)
    age_max = db.Column(db.Integer, nullable=False, default=18)
    #Categories: (level)<int> (gender)<int>
    #gender - male/female
    #level - amateur/intermediate
    #age - 18-/18-49/50+
    #w_class - w:70-/w:70+/m:80-/m:95-/m:90+


    def __repr__(self):
        return {'name': self.name, '': self.id}


class Exercise(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False, default='Noname exercise')  #Name of exercise, to represent
    type = db.Column(db.String(32), nullable=False, default='rest')  #rest/warmup/workout
    max_rep = db.Column(db.Integer, nullable=False, default=0)  #max countable rep, if -1->unlimited
    duration = db.Column(db.Integer, nullable=False, default=0)  #duration of exercise in seconds
    # -------- Connections
    # -------- FK
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    # -------- BACKREF


    def __repr__(self):
        return {'name': self.name, 'type': self.type, 'max': self.max_rep, 'duration': self.duration}
