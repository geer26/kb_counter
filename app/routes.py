from app import app, socket, handler
from flask import request, redirect, render_template, send_from_directory, send_file
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index')
def index():
    if not current_user.is_authenticated:
        return render_template('landingpage.html')
    elif current_user.is_authenticated and current_user.is_superuser:
        return f'Superuser logged in!'
    elif current_user.is_authenticated and not current_user.is_superuser:
        return f'User logged in!'


#websocket connection
@socket.on('connect')
def connect(auth):
    sid = request.sid
    print(f'Somebody connected: <{auth}> with {sid}!')


#websocket event dispatcher
@socket.on('general')
def newmessage(data):

    sid = request.sid

    print(data)

    if data['event'] == 100:
        mess = {}
        mess['event'] = 100
        mess['message'] = data['message']
        socket.emit('general', mess, room=sid)
        return True

