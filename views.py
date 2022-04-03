from flask import Flask,Blueprint,request,url_for,render_template,redirect,flash
from flask_security import login_required,current_user,roles_accepted,current_user
from flask_security.utils import encrypt_password
from models import *
from extensions import *
import json

view = Blueprint('views', __name__)

@view.route('/employeelist', methods=['GET'])
@login_required
@roles_accepted('Manager')
def employeelist():
    users = User.query.all()
    return render_template('employeelist.html',users=users)

@view.route('/managerlist', methods=['GET'])
@login_required
@roles_accepted('Manager')
def managerlist():
    users = User.query.all()
    return render_template('managerlist.html',users=users)

@view.route('/addmanager', methods=['GET','POST'])
@login_required
@roles_accepted('Manager')
def addmanager():
    roles = Role.query.all()
    if request.method == "POST":
        try:
            usr_role = Role.query.get(1)
            new_user = user_datastore.create_user(
                name = request.form['name'],
                email = request.form['email'],
                password = encrypt_password(request.form['password']),
                roles = [usr_role]
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Manager created successfully')
            return redirect(url_for('views.managerlist'))
        except Exception as ae:
            if(str(ae.__dict__['orig']).find("Duplicate entry")!= -1):
                flash("User with this email is already Exist!")
            else:
                flash("Failed to creata a user try again!!")
            logger.exception('Error in adding manager',ae)
    return render_template('addmanager.html')

@view.route('/addemployee', methods=['GET','POST'])
@login_required
@roles_accepted('Manager')
def addemployee():
    roles = Role.query.all()
    if request.method == "POST":
        usr_role = Role.query.get(2)
        new_user = user_datastore.create_user(
            name = request.form['name'],
            email = request.form['email'],
            password = encrypt_password(request.form['password']),
            roles = [usr_role]
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as ae:
            if(str(ae.__dict__['orig']).find("Duplicate entry")!= -1):
                flash("Employee with the entered email is already Exist!")
            else:
                flash("Failed to creata a employee try again!!")
            logger.exception('Error in edit employee',ae)
            return redirect(url_for('views.addemployee'))
        new_employee = Employee(phone=request.form['phone'],designation=request.form['designation'],user=new_user)
        db.session.add(new_employee)
        try:
            db.session.commit()
            flash('Employee created successfully')
            return redirect(url_for('views.employeelist'))
        except Exception as ae:
            if(str(ae.__dict__['orig']).find("Duplicate entry")!= -1):
                flash("Employee with this phone number is already Exist!")
            else:
                flash("Failed to creata a employee try again!!")
            logger.exception('Error in add employee',ae)
            return redirect(url_for('views.addemployee'))
    return render_template('addemployee.html',roles=roles,action="create")

@view.route('/editemployee/<int:id>', methods=['GET','POST'])
@login_required
@roles_accepted('Manager')
def editemployee(id):
    user = User.query.get(id)
    cp_user = user
    if request.method == "POST":
        try:
            usr_role = Role.query.get(2)
            if request.form['name'] != user.name or request.form['email'] != user.email:
                user.name = request.form['name'],
                user.email = request.form['email']
                if 'active' in request.form:
                    user.active = True
                else:
                    user.active = False
                try:
                    db.session.commit()
                except Exception as ae:
                    if(str(ae.__dict__['orig']).find("Duplicate entry")!= -1):
                        flash("Employee with the entered email is already Exist!")
                    else:
                        flash("Failed to edit employee details try again!!")
                    logger.exception('Error in edit employee',ae)
                    return redirect(url_for('views.editemployee', id=id))
            
            emp  = Employee.query.get(user.employee.id)
            if request.form['phone'] != emp.phone or request.form['designation'] != emp.designation:
                emp.phone=request.form['phone']
                emp.designation=request.form['designation']
                db.session.commit()
                flash('Employee updated successfully')
                return redirect(url_for('views.employeelist',))
        except Exception as ae:
            if(str(ae.__dict__['orig']).find("Duplicate entry")!= -1):
                flash("Employee with the entered phone number is already Exist!")
            else:
                flash("Failed to update employee details try again!!")
            logger.exception('Error in edit employee',ae)
            return redirect(url_for('views.editemployee', id=id))
    return render_template('addemployee.html',user=user,action="edit")

@view.route('/viewprofile/<int:id>', methods=['GET','POST'])
@login_required
@roles_accepted('Manager')
def viewprofile(id):
    user = User.query.get(id)
    sk_name = []
    sk_perc = []
    for i in user.employee.skills:
        sk_name.append(i.name)
        sk_perc.append(i.percentage)
    if sk_name == []:
        flash('Employee not added his skills yet')
    return render_template('viewprofile.html',user=user,sk_name=sk_name,sk_perc=sk_perc)

@view.route('/deleteemployee', methods=['DELETE'])
@login_required
@roles_accepted('Manager')
def deleteemployee():
    del_id = str(request.data, 'utf-8')
    try:
        idList = del_id.split(',')
        for id in idList:
            user=user_datastore.get_user(id)
            db.session.delete(user)
            db.session.commit()
        context = {'status':'success'}
    except Exception as ae:
        logger.exception('Error in delete employee',ae)
        context = {'status':'failed'}
    return json.dumps(context)