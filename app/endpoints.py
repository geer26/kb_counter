import json
import os
from datetime import datetime
from flask_restful import Resource
from flask_login import current_user, login_user, logout_user
from flask import request, render_template, send_from_directory, session, Response
from app import api, db
from app.workers import pw_complexity, addsu, adduser, get_all_data, deluser



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
        return get_all_data(), 200



#Done!
class DeleteUser(Resource):
    def post(self):

        #get data from posted json
        json_data = request.get_json(force=True)

        if deluser(json_data):
            return {'status': 0, 'message': 'User deleted!'}, 200
        else:
            return {'status': 1, 'message': f'No user with ID {json_data["id"]}!'}, 500

        return {'status': 9, 'message': 'Something went wrong!'}, 500



#Documented!
class Login(Resource):

    def post(self):

        # get data from posted json
        json_data = request.get_json(force=True)

        #Drop request if there is no payload
        if not json_data:
            return {'status': 4, 'message': 'LOGIN request must have params!'}, 400

        #Drop request in case of missing param
        if not json_data['username'] or not json_data['password']:
            return {'status': 3, 'message': 'Username and password must be presented for login!'}, 400

        username = json_data['username']
        password = json_data['password']

        if 'remember' in json_data.keys():
            remember = json_data['remember']
        else:
            remember = False

        user = Users.query.filter_by(username=str(username)).one_or_none()
        if not user:
            return {'status': 1, 'message': 'Invalid username!'}, 401
        if not user.check_password(str(password)):
            return {'status': 1, 'message': 'Invalid password!'}, 401
        if not user.is_enabled:
            return {'status': 1, 'message': 'User is disabled!'}, 401

        login_user(user, remember=remember)
        #user.authenticated = True
        #user.expiration = int(datetime.now().timedelta(seconds=app.config['LOGIN_EXP_TIME']))
        db.session.commit()

        if user.is_superuser:
            session['role'] = 'admin'
        elif not user.is_superuser:
            session['role'] = 'user'
        session['_id'] = _create_identifier()

        if user.is_superuser:
            return {"status": 0, 'message': 'OK!', "redirect_to": "/admin/", 'role': 'admin', 'username': str(user.username)}, 200
        else:
            return {"status": 0, 'message': 'OK!', "redirect_to": "/user/", 'role': 'user', 'username': str(user.username)}, 200




api.add_resource(AddUser, '/API/adduser')
api.add_resource(GetAllData, '/API/query')
api.add_resource(DeleteUser, '/API/deluser')
api.add_resource(Login, '/API/login')