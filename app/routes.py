from app import app, socket, handler
from flask import request, redirect, render_template, send_from_directory, send_file
from flask_login import current_user, login_user, logout_user, login_required


@app.route( '/', methods=['GET', 'POST'] )
@app.route( '/index', methods=['GET', 'POST'] )
def index():
    if request.method == 'POST' and not current_user.is_authenticated:
        print(request.values)
        return redirect('/')
    else:
        if not current_user.is_authenticated:
            return render_template('landingpage.html')
        elif current_user.is_authenticated and current_user.is_superuser:
            return render_template('superuser/adminindex.html')
        elif current_user.is_authenticated and not current_user.is_superuser:
            return render_template('user/userindex.html')


#websocket connection
@socket.on('connect')
def connect(auth):
    sid = request.sid
    print(f'Somebody connected: <{auth}> with {sid}!')


#websocket event dispatcher
@socket.on('general')
def newmessage(data):

    sid = request.sid

    if data['event'] == 100:
        mess = {}
        mess['event'] = 100
        mess['message'] = data['message']
        socket.emit('general', mess, room=sid)
        return True

