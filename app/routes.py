from app import app
from flask import request, redirect, render_template, send_from_directory, send_file
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/index')
def index():
    if not current_user.is_authenticated:
        return render_template('landingpage.html')
