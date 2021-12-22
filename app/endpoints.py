import json
import os
from datetime import datetime
from flask_restful import Resource
from flask_login import current_user, login_user, logout_user
from flask import request, render_template, send_from_directory, session, Response, redirect
from app import api, db

from app.workers import pw_complexity, addsu, adduser, get_all_data, deluser, add_exercise,\
    del_exercise, get_user_exercises, check_exercise_belonging, mod_exercise, add_workout, \
    get_user_workouts, del_workout, edit_workout, add_event, get_user_events, del_event, \
    swap_event_enable, get_single_event, mod_event, get_settingsmode_data, get_competitorsdata, \
    addcompetitor

from app.models import User, Exercise, Event



def render_whole_userindex_set(userid):
    data = get_settingsmode_data()
    return render_template('user/userindex_set.html', data=data, title='Beállítások'), 200



#Done!
class AddUser(Resource):
    def post(self):

        #get data from posted json
        json_data = request.get_json(force=True)

        #check password complexity
        if not pw_complexity(str(json_data['password'])):
            return {'status': 1, 'message': 'Password to simple, adding user failed!'}, 400

        #check if json has 'su' and/or 'su':1
        if 'su' in json_data.keys() and json_data['su']:
            #want to add superuser
            if addsu(json_data):
                return {'status': 0, 'message': 'Superuser created!'}, 200
            else:
                return {'status': 1, 'message': 'Already has an superuser!'}, 400
        else:
            #want to add user
            if adduser(json_data):
                return {'status': 0, 'message': 'User created!'}, 200
            else:
                return {'status': 1, 'message': 'Create user refused!'}, 400

        return {'status': 9, 'message': 'Something went wrong!'}, 500



#Done!
class GetAllData(Resource):
    def get(self):
        if not current_user.is_authenticated or not current_user.is_superuser:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        return get_all_data(), 200



#Done!
class DeleteUser(Resource):
    def post(self):

        if not current_user.is_authenticated or not current_user.is_superuser:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401

        #get data from posted json
        json_data = request.get_json(force=True)

        if deluser(json_data):
            return {'status': 0, 'message': 'User deleted!'}, 200
        else:
            return {'status': 1, 'message': f'No user with ID {json_data["id"]}!'}, 500

        return {'status': 9, 'message': 'Something went wrong!'}, 500



#Done!
class Login(Resource):

    def post(self):

        if current_user.is_authenticated:
            return {'status': 1, 'message': 'Ön már be van jelentkezve!'}, 400

        # get data from posted json
        json_data = request.get_json(force=True)

        #print(f'POSTED DATA: {json_data}')

        #Drop request if there is no payload
        if not json_data:
            return {'status': 4, 'message': 'Hiányzó kötelező mezők!'}, 400

        #Drop request in case of missing param
        if not json_data['username'] or not json_data['password']:
            return {'status': 3, 'message': 'Hiányzó kötelező mezők!'}, 400

        #Extract creditentials from payload
        username = json_data['username']
        password = json_data['password']
        mode = json_data['mode']

        #Deprecated, will be False as default!
        '''
        if 'remember' in json_data.keys():
            remember = json_data['remember']
        else:
            remember = False
        '''

        #Filter user by username
        user = User.query.filter_by(username=str(username)).one_or_none()
        #Return 401 by invalid username
        if not user:
            return {'status': 1, 'message': 'Hibás azonsító adat!'}, 401
        #Return 401 by invalid password
        if not user.check_password(str(password)):
            return {'status': 1, 'message': 'Hibás azonsító adat!'}, 401

        #If OK, log user in and return 200
        login_user(user, remember=False)
        #Edit cookies and session here!
        session['_mode'] = mode
        return {"status": 0, 'message': f'User {user.username} logged in!'}, 200



#Done!
class Add_exercise(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        # call worker that adds record
        if add_exercise(json_data):

            # compose fragment to replace old
            data = get_user_exercises(json_data['userid'])
            fragment = render_template('user/fragments/frag_exercises.html', data=data)
            # return the rendered fragment
            return {'status': 0, 'message': 'Sikeres művelet!', 'fragment': fragment}, 200

        else:
            # something - somewhere went wrong!
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#Done!
class Del_exercise(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        # call worker that deletes record
        if del_exercise(json_data):

            # compose fragment to replace old
            data = get_user_exercises(json_data['userid'])
            fragment = render_template('user/fragments/frag_exercises.html', data=data)
            # return the rendered fragment
            #return {'status': 0, 'message': 'Sikeres művelet!', 'fragment': fragment}, 200
            return '', 200

        else:
            # something - somewhere went wrong!
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#Done!
class Get_exercise(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        # call worker that deletes record
        if not 'exid' in json_data:
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500
        data = Exercise.query.get(int(json_data['exid'])).get_self_json()
        return data , 200



#Done - Document it!
class Modify_exercise(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        # DATA contains: {'id': 5, 'name': 'test2', 'short_name': 't2', 'link': 'frgefg', 'type': 'warmup', 'max_rep': 234, 'duration': 456, 'user': 2}
        # check if record belongs to user
        if not check_exercise_belonging(int(json_data['id'])):
            return {'status': 1, 'message': 'Nem jogosult a művelet végrehajtására!'}, 401
        # call worker that modifies record
        if mod_exercise(json_data):
            # compose fragment to replace old
            data = get_user_exercises(json_data['user'])
            fragment = render_template('user/fragments/frag_exercises.html', data=data)
            # return the rendered fragment
            return {'status': 0, 'message': 'Sikeres művelet!', 'fragment': fragment}, 200
        else:
            # something - somewhere went wrong!
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#Done - Document it!
class Add_workout(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        # call worker that modifies record
        if add_workout(json_data):
            # compose fragment to replace old
            data = get_user_workouts(json_data['user'])
            fragment = render_template('user/fragments/frag_workouts.html', data=data)
            # return the rendered fragment
            return {'status': 0, 'message': 'Sikeres művelet!', 'fragment': fragment}, 200
        else:
            # something - somewhere went wrong!
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#Done!
class Del_workout(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        if current_user.id != int(json_data['userid']) and not current_user.is_superuser:
            return {'status': 1, 'message': 'Nem jogosult a művelet végrehajtására!'}, 403
        # call worker that deletes record
        if del_workout(json_data):
            # compose fragment to replace old
            data = get_user_workouts(json_data['userid'])
            fragment = render_template('user/fragments/frag_workouts.html', data=data)
            # return the rendered fragment
            #return {'status': 0, 'message': 'Sikeres művelet!', 'fragment': fragment}, 200
            return '',200
        else:
            # something - somewhere went wrong!
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#Done - Document it!
class Update_workout(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        if current_user.id != int(json_data['user']) and not current_user.is_superuser:
            return {'status': 1, 'message': 'Nem jogosult a művelet végrehajtására!'}, 403
        # call worker that modifies record
        if edit_workout(json_data):
            # compose fragment to replace old
            data = get_user_workouts(json_data['user'])
            fragment = render_template('user/fragments/frag_workouts.html', data=data)
            # return the rendered fragment
            return {'status': 0, 'message': 'Sikeres művelet!', 'fragment': fragment}, 200
        else:
            # something - somewhere went wrong!
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#Done - Document it!
class Add_event(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        # call worker that modifies record
        if add_event(json_data):
            # compose fragment to replace old
            data = get_user_events(json_data['user'])
            fragment = render_template('user/fragments/frag_events.html', data=data)
            # return the rendered fragment
            return {'status': 0, 'message': 'Sikeres művelet!', 'fragment': fragment}, 200
        else:
            # something - somewhere went wrong!
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#Done!
class Del_event(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        if current_user.id != int(json_data['userid']) and not current_user.is_superuser:
            return {'status': 1, 'message': 'Nem jogosult a művelet végrehajtására!'}, 403
        # check if event is closed
        e = Event.query.get(int(json_data['id']))
        if e.closed: return {'status': 1, 'message': 'Lezárt eseményt nem törölhet!'}, 403
        # call worker that deletes record
        if del_event(json_data):
            # compose fragment to replace old
            data = get_user_events(json_data['userid'])
            fragment = render_template('user/fragments/frag_events.html', data=data)
            # return the rendered fragment
            return {'status': 0, 'message': 'Sikeres művelet!', 'fragment': fragment}, 200
        else:
            # something - somewhere went wrong!
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#Done!
class Swap_enabled(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        if current_user.id != int(json_data['userid']) and not current_user.is_superuser:
            return {'status': 1, 'message': 'Nem jogosult a művelet végrehajtására!'}, 403
        # call worker that deletes record
        if swap_event_enable(json_data):
            # compose fragment to replace old
            data = get_user_events(json_data['userid'])
            fragment = render_template('user/fragments/frag_events.html', data=data)
            # return the rendered fragment
            return {'status': 0, 'message': 'Sikeres művelet!', 'fragment': fragment}, 200
        else:
            # something - somewhere went wrong!
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#Done - Document it!
class Get_eventdata(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        if current_user.id != int(json_data['userid']) and not current_user.is_superuser:
            return {'status': 1, 'message': 'Nem jogosult a művelet végrehajtására!'}, 403
        # check if event is closed
        e = Event.query.get(int(json_data['id']))
        if e.closed: return {'status': 1, 'message': 'Lezárt eseményt nem módosíthat!'}, 403
        # call worker that reads the event record
        try:
            return { 'status': 0, 'message': 'Sikeres művelet!', 'data': get_single_event(json_data['id']) }, 200
        except:
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#Done
class Edit_event(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
        # get data from posted json
        json_data = request.get_json(force=True)
        if current_user.id != int(json_data['userid']) and not current_user.is_superuser:
            return {'status': 1, 'message': 'Nem jogosult a művelet végrehajtására!'}, 403
        # check if event is closed
        e = Event.query.get(int(json_data['id']))
        if e.closed: return {'status': 1, 'message': 'Lezárt eseményt nem módosíthat!'}, 403
        # call worker that reads the event record
        if mod_event(json_data):
            # compose fragment to replace old
            data = get_user_events(json_data['userid'])
            fragment = render_template('user/fragments/frag_events.html', data=data)
            # return the rendered fragment
            return {'status': 0, 'message': 'Sikeres művelet!', 'fragment': fragment}, 200
        else:
            # something - somewhere went wrong!
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#TODO work on this!!!
class Get_comps_fragment(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
            # get data from posted json
        json_data = request.get_json(force=True)
        if current_user.id != int(json_data['userid']) and not current_user.is_superuser:
            return {'status': 1, 'message': 'Nem jogosult a művelet végrehajtására!'}, 403
        # check if event is closed
        e = Event.query.get(int(json_data['id']))
        if e.closed: return {'status': 1, 'message': 'Lezárt eseményt nem módosíthat!'}, 403
        try:
            data = get_competitorsdata(json_data)
            if not data:
                return {'status': 1, 'message': 'Sikertelen művelet!'}, 500
            response = render_template('user/fragments/frag_manipulate_comps.html', cdata=data)
            return {'status': 0, 'message': 'Sikeres művelet', 'fragment': response}, 200
        except:
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



#TODO Get this!!!
class Add_competitor(Resource):
    def post(self):
        if not current_user.is_authenticated:
            return {'status': 1, 'message': 'A művelet végrehajtásához jelentkezzen be!'}, 401
            # get data from posted json
        json_data = request.get_json(force=True)
        if current_user.id != int(json_data['userid']) and not current_user.is_superuser:
            return {'status': 1, 'message': 'Nem jogosult a művelet végrehajtására!'}, 403
        # check if event is closed
        e = Event.query.get(int(json_data['eventid']))
        if e.closed: return {'status': 1, 'message': 'Lezárt eseményt nem módosíthat!'}, 403
        if addcompetitor(json_data):
            return {'status': 0, 'message': 'Sikeres művelet'}, 200
        else:
            return {'status': 1, 'message': 'Sikertelen művelet!'}, 500



api.add_resource(AddUser, '/API/adduser')
api.add_resource(GetAllData, '/API/query')
api.add_resource(DeleteUser, '/API/deluser')
api.add_resource(Login, '/API/login')
api.add_resource(Add_exercise, '/API/addexercise')
api.add_resource(Del_exercise, '/API/delexercise')
api.add_resource(Get_exercise, '/API/getexercise')
api.add_resource(Modify_exercise, '/API/modifyexercise')
api.add_resource(Add_workout, '/API/addworkout')
api.add_resource(Del_workout, '/API/delworkout')
api.add_resource(Update_workout, '/API/updateworkout')
api.add_resource(Add_event, '/API/addevent')
api.add_resource(Del_event, '/API/delevent')
api.add_resource(Swap_enabled, '/API/swapenable')
api.add_resource(Edit_event, '/API/editevent')
api.add_resource(Get_eventdata, '/API/geteventdata')
api.add_resource(Get_comps_fragment, '/API/getcompfragment')
api.add_resource(Add_competitor, '/API/addcompetitor')