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
        for comp in Competitor.query.filter_by(workout=workout.id):
            db.session.delete(comp)
            db.session.commit()
        # get to events and delete from workouts list
        del_w_from_ev_list(str(id))
        db.session.delete(workout)
        db.session.commit()
        return True
    except:
        return False


def del_w_from_ev_list(id):

    print(f'IN del_w_fro_ev_list FUNCTION')
    for event in Event.query.all():
        list = json.loads(event.workouts)
        if id not in list:
            continue

        while id in list: list.remove(id)
        if len(list) < 1:
            del_event({'id': event.id})
            db.session.commit()
            continue

        #del competitors from this workout
        #int_id = int(id)
        #for competitor in Competitor.query.filter_by(workout=int_id).all():
        #    db.session.remove(competitor)
        #    db.session.commit()

        seq = json.loads(event.sequence)
        seq.pop( id , None )
        event.sequence = json.dumps(seq)

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



def mod_event(data):
    try:
        event = Event.query.get(int(data['id']))
        event.short_name = data['short_name']
        event.description = data['description']
        event.named = data['named']
        event.workouts = json.dumps(data['list_of_workouts'])

        temp_sequence = {}
        live_sequence = json.loads(event.sequence)

        for workout in data['list_of_workouts']:
            if workout in live_sequence.keys():
                temp_sequence[workout] = live_sequence[workout]
            else:
                temp_sequence[workout] = []

        for key in live_sequence.keys():
            if key not in temp_sequence.keys():
                comps = live_sequence[key]
                for c in comps:
                    db.session.delete(Competitor.query.get(int(c)))

        event.sequence = json.dumps(temp_sequence)

        db.session.commit()
        return True
    except:
        return False



def update_sequence(data):
    try:
        event = Event.query.get(int(data['eventid']))
        event.sequence = json.dumps(data['sequence'])
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



def get_competitorsdata(data):
    try:
        d = {}
        event = Event.query.get(int(data['id']))
        event_sequence = json.loads(event.sequence)

        d['eventname'] = event.short_name
        d['eventid'] = event.id

        d['workout_names'] = []

        for workout in json.loads(event.workouts):
            wo = {}
            work = Workout.query.get(int(workout))
            wo['id'] = work.id
            wo['name'] = work.short_name
            wo['comps'] = len(json.loads(event.sequence)[str(work.id)])

            wo['competitors'] = []
            for competitor in json.loads(event.sequence)[str(work.id)]:
                cid = int(competitor)
                comp = Competitor.query.get(cid).get_self_json()
                wo['competitors'].append(comp)

            d['workout_names'].append(wo)

        return d
    except:
        return False



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



def get_competitordata(data):
    try:
        #print(data)
        #{'cid': 2, 'userid': 2}
        competitor = Competitor.query.get(int(data['cid']))
        d = json.dumps(competitor.get_self_json())
        return d
    except:
        return False



def modcompetitor(data):
    try:
        print(data)
        #{'compid': 1, 'eventid': 1, 'userid': 2, 'cname': 'adr', 'association': '', 'weight': 343, 'y_o_b': 234, 'gender': 2, 'workout': '2'}
        #TODO modify event.sequence also!!!

        '''
        competitor = Competitor.query.get(int(data['compid']))
        competitor.cname = str(data['cname'])
        competitor.association = str(data['association'])
        competitor.weight = int(data['weight'])
        competitor.y_o_b = int(data['y_o_b'])
        competitor.gender = int(data['gender'])
        competitor.workout = int(data['workout'])
        competitor.event = int(data['eventid'])
        competitor.generate_category()
        db.session.commit()
        '''
        return True
    except:
        return False



def fetch_userevents(userid):
    events = []
    for event in Event.query.filter_by(user = int(userid)):
        events.append({'eid': event.id, 'eventname': event.short_name, 'playable': not event.closed, 'named': event.named})
    return json.dumps(events)



def fetch_event(eventid):
    # desired structure: [ {competitor data, 'exercises:[ {exercise data}, ... ]'}, ... ]
    data_to_return = []
    # select event
    e = Event.query.get(int(eventid))
    # get workout sequence in the event
    workout_sequence = json.loads(e.workouts)
    #get competitors sequence
    competitor_sequence = json.loads(e.sequence)
    # get competitors in sequence
    for workout in workout_sequence:
        w = Workout.query.get(int(workout))
        for compid in competitor_sequence[workout]:
            c = Competitor.query.get(int(compid))
            cid = c.id
            cname = c.cname
            cassoc = c.association
            # get exercises to fullfil
            exercises = []
            for exercise in json.loads(w.exercises):
                ex = {}
                e = Exercise.query.get(int(exercise))
                ex['ename'] = e.short_name
                ex['type'] = e.type
                ex['max_rep'] = e.max_rep
                ex['duration'] = e.duration
                exercises.append(ex)

            data_to_return.append({'cid':cid, 'cname': cname, 'cassoc': cassoc, 'exercises':exercises})


    #print(f'DATA TO WORK WITH: {data_to_return}')

    return data_to_return