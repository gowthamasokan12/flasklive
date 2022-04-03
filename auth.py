from flask import Flask,Blueprint,url_for,render_template,redirect
from flask_security import login_required,current_user
from views import view

auths = Blueprint('auth', __name__)

@auths.route('/', methods=['GET','POST'])
def login():
    return redirect(url_for('security.login'))

@auths.route('/index', methods=['GET','POST'])
@login_required
def index():
    if 'Manager' in current_user.roles:
        return redirect(url_for('views.employeelist'))
    else:
        return redirect(url_for('emp.profile'))

@auths.route('/logout', methods=['GET','POST'])
def logout():
    return redirect(url_for('security.logout'))