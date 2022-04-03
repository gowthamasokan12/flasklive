from flask import Flask,Blueprint,request,url_for,render_template,redirect,flash
from flask_security import login_required,current_user,roles_accepted,current_user
from flask_security.utils import encrypt_password
from models import *
from extensions import *
import json

emp = Blueprint('emp', __name__)

@emp.route('/addskill', methods=['GET','POST'])
@login_required
@roles_accepted('Employee')
def addskill():
    if request.method == 'POST':
        flt = Skill.query.filter_by(name=request.form['skill'],employee=current_user.employee).first()
        
        if flt == None:
            try:
                new_skill = Skill(
                    name=request.form['skill'],
                    percentage=int(request.form['percent']),
                    employee = current_user.employee
                )
                db.session.add(new_skill)
                db.session.commit()
                flash('Skill added successfully')
                return redirect(url_for('emp.profile'))
            except Exception as ae:
                logger.exception('Error in add skill',ae)
                flash('Failed to add skill try again!')
        else:
            flash('Skill Already Exist!')
    return render_template('addskill.html',action="create")

@emp.route('/editskill/<int:id>', methods=['GET','POST'])
@login_required
@roles_accepted('Employee')
def editskill(id):
    skill = Skill.query.get(id)
    if request.method == 'POST':
        try:
            skill.name=request.form['skill']
            skill.percentage=int(request.form['percent'])
            
            db.session.commit()
            flash('Skill updated successfully')
            return redirect(url_for('emp.profile'))
        except Exception as ae:
            flash('Failed to update try again!')
            logger.exception('Error in edit skill',ae)
    return render_template('addskill.html',skill=skill,action="edit")

@emp.route('/deleteskill', methods=['DELETE'])
@login_required
@roles_accepted('Employee')
def deleteskill():
    del_id = str(request.data, 'utf-8')
    try:
        idList = del_id.split(',')
        for id in idList:
            skill=Skill.query.get(id)
            db.session.delete(skill)
            db.session.commit()
        context = {'status':'success'}
    except Exception as ae:
        logger.exception('Error in delete skill',ae)
        context = {'status':'failed'}
    return json.dumps(context)

@emp.route('/profile', methods=['GET'])
@login_required
def profile():
    sk_name = []
    sk_perc = []
    if 'Employe' in current_user.roles:
        for i in current_user.employee.skills:
            sk_name.append(i.name)
            sk_perc.append(i.percentage)
    return render_template('profile.html',sk_name=sk_name,sk_perc=sk_perc)

@emp.route('/employee', methods=['GET','POST'])
@login_required
def employee():
    return 'employee'