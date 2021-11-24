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




api.add_resource(AddUser, '/API/adduser')
api.add_resource(GetAllData, '/API/query')
api.add_resource(DeleteUser, '/API/deluser')