from app import app, socket, handler
from flask import request, redirect, render_template, send_from_directory, send_file, session
from flask_login import current_user, login_user, logout_user, login_required
from app.workers import get_settingsmode_data


@app.route( '/', methods=['GET', 'POST'] )
@app.route( '/index', methods=['GET', 'POST'] )
def index():
    if request.method == 'POST' and not current_user.is_authenticated:
        #print(request.values)
        return redirect('/')
    else:
        #print(session)
        if not current_user.is_authenticated:
            return render_template('landingpage.html')
        elif current_user.is_authenticated and current_user.is_superuser:
            return render_template('superuser/adminindex.html')
        elif current_user.is_authenticated and not current_user.is_superuser and session['_mode'] == 'SET' :
            data = get_settingsmode_data()
            print(data)
            return render_template('user/userindex_set.html', data=data, title='Beállítások')
        elif current_user.is_authenticated and not current_user.is_superuser and session['_mode'] == 'EXC' :
            return render_template('user/userindex_exc.html')
        elif current_user.is_authenticated and not current_user.is_superuser and session['_mode'] == 'SIN' :
            return render_template('user/userindex_sin.html')
        elif current_user.is_authenticated and not current_user.is_superuser and session['_mode'] == 'COO' :
            return render_template('user/userindex_coo.html')
        else:
            return '', 404


@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect('/')


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

