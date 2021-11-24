import json
from app import db
from app.models import User



def pw_complexity(pw):
    pw_ok = True

    return pw_ok


def addsu(data):
    for user in User.query.all():
        if user.is_superuser: return False

    user = User()
    username = data['username'][:32]
    password = data['password']

    user.username=username
    user.set_password(password)
    user.is_superuser = True

    db.session.add(user)
    db.session.commit()

    return True


def adduser(data):
    user = User()
    username = data['username'][:32]
    password = data['password']

    user.username = username
    user.set_password(password)
    user.is_superuser = False

    db.session.add(user)
    db.session.commit()
    return True


def get_all_data():
    data = {}

    data['USERS'] = []
    for user in User.query.all():
        data['USERS'].append(user.get_self_json())

    return data