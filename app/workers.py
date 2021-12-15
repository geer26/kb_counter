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
    for user in User.query.all() : data['USERS'].append(user.get_self_json())

    data['EXERCISES'] = []
    for exercise in Exercise.query.all() : data['EXERCISES'].append(exercise.get_self_json())

    data['WORKOUTS'] = []
    for workout in Workout.query.all(): data['WORKOUTS'].append(workout.get_self_json())

    data['EVENTS'] = []
    for event in Event.query.all(): data['EVENTS'].append(event.get_self_json())

    data['COMPETITORS'] = []
    for competitor in Competitor.query.all(): data['COMPETITORS'].append(competitor.get_self_json())

    return data


def get_settingsmode_data():
    data = {}

    userid = int(current_user.id)

    data['user'] = User.query.get(userid).get_self_json()

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

    return data


def get_user_exercises(userid):
    userid = int(userid)
    data = {}
    data['exercises'] = []
    for exercise in Exercise.query.filter_by(user=userid).all():
        data['exercises'].append(exercise)
    return data


def get_user_workouts(userid):
    userid = int(userid)
    data = {}
    data['workouts'] = []
    for workout in Workout.query.filter_by(user=userid).all():
        data['workouts'].append(workout.get_self_json())
    return data


def get_user_events(userid):
    userid = int(userid)
    data = {}
    data['events'] = []
    for event in Event.query.filter_by(user=userid).all():
        d = event.get_self_json()
        d['competitors'] = []
        for competitor in Competitor.query.all():
            if competitor.event == int(d['id']): d['competitors'].append(competitor)
        data['events'].append(d)
    return data


def add_exercise(data):
    #{name: name, short_name: short_name, link: link, type: type, max_rep:max_rep, duration:duration, userid:userid}
    try:
        exercise = Exercise()
        exercise.name = data['name']
        exercise.short_name = data['short_name']
        exercise.link = data['link']
        exercise.type = data['type']
        exercise.max_rep = data['max_rep']
        exercise.duration = data['duration']
        exercise.user = int(data['userid'])
        db.session.add(exercise)
        db.session.commit()
        return True
    except:
        return False


def del_exercise(data):
    try:
        id = int(data['id'])
        db.session.delete(Exercise.query.get(id))
        db.session.commit()
        return True
    except:
        return False


def check_exercise_belonging(id):
    return Exercise.query.get(int(id)).user == current_user.id


def mod_exercise(data):
    # DATA contains: {'id': 5, 'name': 'test2', 'short_name': 't2', 'link': 'frgefg', 'type': 'warmup', 'max_rep': 234, 'duration': 456, 'user': 2}
    try:
        exercise = Exercise.query.get(int(data['id']))
        exercise.name = data['name']
        exercise.short_name = data['short_name']
        exercise.link = data['link']
        exercise.type = data['type']
        exercise.max_rep = data['max_rep']
        exercise.duration = data['duration']
        db.session.commit()
    except:
        return False
    return True


def add_workout(data):
    try:
        workout = Workout()
        workout.short_name = data['short_name']
        workout.description = data['description']
        workout.exercises = json.dumps(data['exercises'])
        workout.user = data['user']
        db.session.add(workout)
        db.session.commit()
        return True
    except:
        return False


def del_workout(data):
    try:
        id = int(data['id'])
        db.session.delete(Workout.query.get(id))
        db.session.commit()
        return True
    except:
        return False


def edit_workout(data):
    try:
        workout = Workout.query.get(int(data['woid']))
        workout.short_name = str(data['short_name'])
        workout.description = str(data['description'])
        workout.exercises = json.dumps(data['exercises'])
        db.session.commit()
        return True
    except:
        return False


def add_event(data):
    try:
        event = Event()
        event.short_name = data['short_name']
        event.description = data['description']
        event.workouts = json.dumps(data['workouts'])
        event.user = data['user']
        event.gen_ident()
        db.session.add(event)
        db.session.commit()
        return True
    except:
        return False


def del_event(data):
    try:
        id = int(data['id'])
        db.session.delete(Event.query.get(id))
        db.session.commit()
        return True
    except:
        return False



#TODO implement nullpointer safety on delete!!!