import json
from app import db
from app.models import User, Event, Workout, Competitor, Exercise
from flask_login import current_user



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


def deluser(data):
    user = User.query.get(int(data['id']))
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True


def get_all_data():
    data = {}

    data['USERS'] = []
    for user in User.query.all():
        data['USERS'].append(user.get_self_json())

    return data


def get_settingsmode_data():
    data = {}

    userid = int(current_user.id)
    print(userid)

    data['user'] = User.query.get(userid).get_self_json()
    print(data['user'])

    data['events'] = []
    for event in Event.query.filter_by(user=userid).all():
        e = event.get_self_json()
        e['competitors'] = []
        for competitor in Competitor.query.filter_by(event=event.id).all():
            e['competitors'].append(competitor.get_self_json())
        data['events'].append(e)

    data['workouts'] = []
    for workout in Workout.query.filter_by(user=userid).all():
        data['workouts'].append(workout.get_self_json())

    data['exercises'] = []
    for exercise in Exercise.query.filter_by(user=userid).all():
        data['exercises'].append(exercise)

    print(data)

    return data