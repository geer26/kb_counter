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


def get_single_event(id):
    id = int(id)
    event = Event.query.get(id)
    data = {
        'ev_id': id,
        'ev_sname': event.short_name,
        'ev_description': event.description,
        'ev_ident': event.ident,
        'ev_workouts': json.loads(event.workouts),
        'ev_named': event.named
    }
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
        exercise = Exercise.query.get(id)
        #get to workouts and delete from exercise list
        del_ex_from_w_list(id)
        db.session.delete(exercise)
        db.session.commit()
        return True
    except:
        return False


def del_ex_from_w_list(id):

    id = str(id)

    for workout in Workout.query.all():
        list = json.loads(workout.exercises)
        if id not in list:
            continue

        while id in list: list.remove(id)
        if len(list) < 1:
            del_workout({'id': workout.id})
            db.session.commit()
            continue

        workout.exercises = json.dumps(list)
        db.session.commit()

    return True


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
        workout = Workout.query.get(id)
        # del competitors with the same workout
        #for comp in Competitor.query.filter_by(workout=workout.id):
        #    db.session.delete(comp)
        #    db.session.commit()
        # get to events and delete from workouts list
        del_w_from_ev_list(id)
        db.session.delete(workout)
        db.session.commit()
        return True
    except:
        return False


def del_w_from_ev_list(id):

    id = str(id)

    for event in Event.query.all():
        list = json.loads(event.workouts)
        if id not in list:
            continue

        while id in list: list.remove(id)
        if len(list) < 1:
            del_event({'id': event.id})
            db.session.commit()
            continue

        event.workouts = json.dumps(list)
        db.session.commit()

    return True


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


#TODO recreate with event.sequence!
def add_event(data):
    try:
        event = Event()
        event.short_name = data['short_name']
        event.description = data['description']
        event.workouts = json.dumps(data['workouts'])
        seq = {}
        for wo in data['workouts']:
            seq[str(wo)] = []
        event.sequence =json.dumps(seq)
        event.user = data['user']
        event.named = data['named']
        event.gen_ident()
        db.session.add(event)
        db.session.commit()
        return True
    except:
        return False


#TODO recreate with event.sequence!
def del_event(data):
    try:
        id = int(data['id'])
        e = Event.query.get(id)
        if e.closed: return False
        # delete connected competitors
        for comp in Competitor.query.filter_by(event=e.id):
            db.session.delete(comp)
            db.session.commit()
        db.session.delete(e)
        db.session.commit()
        return True
    except:
        return False


#TODO recreate with event.sequence!
def mod_event(data):
    try:
        event = Event.query.get(int(data['id']))
        event.short_name = data['short_name']
        event.description = data['description']
        event.named = data['named']
        event.workouts = json.dumps(data['list_of_workouts'])
        db.session.commit()
        return True
    except:
        return False


def swap_event_enable(data):
    try:
        id = int(data['id'])
        event = Event.query.get(id)
        event.closed = not event.closed
        db.session.commit()
        return True
    except:
        return False


#TODO recreate with event.sequence!
def get_competitorsdata(data):
    try:
        d = {}
        event = Event.query.get(int(data['id']))

        d['eventname'] = event.short_name
        d['eventid'] = event.id

        d['workout_names'] = []
        for workout in json.loads(event.workouts):
            wdata = {}
            wo = Workout.query.get(int(workout))
            wdata['id'] = workout
            wdata['name'] = wo.short_name
            wdata['comps'] = 0
            #get competitors number by workout
            comps = Competitor.query.filter_by(workout=workout).all()
            wdata['comps'] = len(comps)
            #get relevant competitors
            wdata['competitors'] = []
            for competitor in Competitor.query.filter_by(event=event.id).filter_by(workout=workout).all():
                #print(competitor.get_self_json())
                wdata['competitors'].append(competitor.get_self_json())
            d['workout_names'].append(wdata)

        return d
    except:
        return False


#TODO recreate with event.sequence!
def addcompetitor(data):
    try:
        #print(data)
        #{'eventid': 1, 'userid': 2, 'cname': 'adr', 'association': '', 'weight': 343, 'y_o_b': 234, 'gender': 2, 'workout': '2'}
        competitor = Competitor()
        competitor.cname = str(data['cname'])
        competitor.association = str(data['association'])
        competitor.weight = int(data['weight'])
        competitor.y_o_b = int(data['y_o_b'])
        competitor.gender = int(data['gender'])
        competitor.workout = int(data['workout'])
        competitor.event = int(data['eventid'])
        competitor.generate_category()
        db.session.add(competitor)
        db.session.commit()

        event = Event.query.get(int(data['eventid']))
        seq = json.loads(event.sequence)
        seq[str(data['workout'])].append(str(competitor.id))
        event.sequence = json.dumps(seq)

        db.session.commit()
        return True
    except:
        return False


#TODO recreate with event.sequence!
def modcompetitor(data):
    try:
        #print(data)
        #{'compid': 1, 'eventid': 1, 'userid': 2, 'cname': 'adr', 'association': '', 'weight': 343, 'y_o_b': 234, 'gender': 2, 'workout': '2'}
        competitor = Competitor.query.get(int(data['compid']))
        competitor.cname = str(data['cname'])
        competitor.association = str(data['association'])
        competitor.weight = int(data['weight'])
        competitor.y_o_b = int(data['y_o_b'])
        competitor.gender = int(data['gender'])
        competitor.workout = int(data['workout'])
        competitor.event = int(data['eventid'])
        competitor.generate_category()
        db.session.add(competitor)
        db.session.commit()
        return True
    except:
        return False