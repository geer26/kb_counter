from app import app, socket
from flask import request, redirect, render_template, send_from_directory, send_file
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/index')
def index():
    if not current_user.is_authenticated:
        return render_template('landingpage.html')


#websocket event dispatcher
@socket.on('newmessage')
def newmessage(data):

    sid = request.sid

'''
    #incoming request for error message with message - DONE
    if data['event'] == 291:
        mess = {}
        mess['event'] = 191
        mess['htm'] = render_template('errormessage.html', message=data['message'])
        socket.emit('newmessage', mess, room=sid)
        return True


    #Experimental details
    #request for details view
    if data['event'] == 293 and current_user.is_authenticated:

        pid = int(data['pid'])
        pocket = Pocket.query.get(pid)

        transfers = Transfer.query.filter_by(_pocket=pocket).order_by(Transfer.timestamp).all()

        if len(transfers) < 1:
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='No tansfers in this pocket!')
            socket.emit('newmessage', mess, room=sid)
            return False

        daterange = {}
        daterange['min'] = transfers[0].timestamp.timestamp()*1000
        daterange['max'] = transfers[-1].timestamp.timestamp()*1000

        temp = {}
        temp['pid'] = pid
        temp['min'] = transfers[0].timestamp
        temp['max'] = transfers[-1].timestamp

        charts = drawcharts2(temp)

        mess = {}
        mess['event'] = 193
        mess['htm'] = render_template('details2.html',
                                      p=pid,
                                      pocket=pocket,
                                      user=current_user,
                                      daterange=daterange,
                                      charts=charts,
                                      transfers=transfers)
        socket.emit('newmessage', mess, room=sid)

        return True


    #refresh details daterange
    if data['event'] == 294 and current_user.is_authenticated:

        pid = int(data['pid'])

        fromdate = datetime.fromtimestamp(int(data['mintime']/1000), tz=pytz.utc)
        todate = datetime.fromtimestamp(int(data['maxtime']/1000), tz=pytz.utc)

        pocket = Pocket.query.get(pid)
        transfers = Transfer.query.filter_by(_pocket=pocket).order_by(Transfer.timestamp).filter(
            Transfer.timestamp >= fromdate).filter(Transfer.timestamp <= todate).all()

        newdate = {}
        newdate['min'] = transfers[0].timestamp.timestamp() * 1000
        newdate['max'] = transfers[-1].timestamp.timestamp() * 1000

        temp = {}
        temp['pid'] = pid
        temp['min'] = fromdate
        temp['max'] = todate

        charts = drawcharts2(temp)

        mess = {}
        mess['event'] = 194
        mess['htm'] = render_template('charts.html', charts=charts, transfers=transfers, newdate=newdate)
        socket.emit('newmessage', mess, room=sid)
        return True
'''

