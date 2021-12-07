import json
import os
from datetime import datetime
from flask_restful import Resource
from flask_login import current_user, login_user, logout_user
from flask import request, render_template, send_from_directory, session, Response
from app import api, db
from app.workers import pw_complexity, addsu, adduser, get_all_data, deluser
from app.models import User



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



#Done!
class Login(Resource):

    def post(self):

        #return '',200

        # get data from posted json
        json_data = request.get_json(force=True)

        print(f'POSTED DATA: {json_data}')

        #Drop request if already logged in
        if current_user.is_authenticated:
            return {'status': 2, 'message': 'Already logged in!'}, 400

        #Drop request if there is no payload
        if not json_data:
            return {'status': 4, 'message': 'LOGIN request must have params!'}, 400

        #Drop request in case of missing param
        if not json_data['username'] or not json_data['password']:
            return {'status': 3, 'message': 'Username and password must be presented for login!'}, 400

        #Extract creditentials from payload
        username = json_data['username']
        password = json_data['password']

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
            return {'status': 1, 'message': 'Invalid username!'}, 401
        #Return 401 by invalid password
        if not user.check_password(str(password)):
            return {'status': 1, 'message': 'Invalid password!'}, 401

        #If OK, log user in and return 200
        login_user(user, remember=False)
        #Edit cookies and session here!
        return {"status": 0, 'message': f'User {user.username} logged in!'}, 200



#Done!
class Logout(Resource):
    def get(self):

        if not current_user or not current_user.is_authenticated:
            return {'status': 1, 'message': 'User already logged out!'}, 400
        username = current_user.username
        if logout_user():
            return {'status': 0, 'message': f'User {username} logged out!'}, 200
        else:
            {'status': 2, 'message': f'Server error occured!'}, 500




api.add_resource(AddUser, '/API/adduser')
api.add_resource(GetAllData, '/API/query')
api.add_resource(DeleteUser, '/API/deluser')
api.add_resource(Login, '/API/login')
api.add_resource(Logout, '/API/logout')