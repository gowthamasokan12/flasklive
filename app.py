from flask import Flask,request,url_for,render_template,redirect,session,flash
import os,json,logging
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required, UserMixin, RoleMixin, roles_accepted,current_user
from flask_security.utils import encrypt_password
from flask_migrate import Migrate


app=Flask(__name__)
app.config.from_pyfile('config.py')

logger=logging.getLogger()
logging.basicConfig(filename="newfile.log",format='%(asctime)s %(message)s',  filemode='w') 

db = SQLAlchemy(app)
migrate = Migrate(app, db)


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'),unique=True),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    roles= db.relationship('Role', secondary=roles_users,
                            backref=db.backref('user', lazy='dynamic'))
    employee = db.relationship('Employee',backref="user",uselist=False)


    def __str__(self):
        return self.email

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    phone = db.Column(db.String(255), unique=True, nullable=False)
    designation = db.Column(db.String(255), nullable=False)
    skills = db.relationship('Skill',backref='employee')
    users = db.relationship('User',back_populates="employee")

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer(), db.ForeignKey('employee.id'))
    name = db.Column(db.String(255), nullable=False)
    percentage = db.Column(db.Integer, nullable=False)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/', methods=['GET','POST'])
def login():
    return redirect(url_for('security.login'))

@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    if 'Manager' in current_user.roles:
        return redirect(url_for('employeelist'))
    else:
        return redirect(url_for('profile'))

@app.route('/employeelist', methods=['GET'])
@login_required
@roles_accepted('Manager')
def employeelist():
    users = User.query.all()
    return render_template('employeelist.html',users=users)

@app.route('/managerlist', methods=['GET'])
@login_required
@roles_accepted('Manager')
def managerlist():
    users = User.query.all()
    return render_template('managerlist.html',users=users)

@app.route('/addmanager', methods=['GET','POST'])
@login_required
@roles_accepted('Manager')
def addmanager():
    roles = Role.query.all()
    print(roles)
    if request.method == "POST":
        print(request.form['name'])
        try:
            usr_role = Role.query.get(1)
            print(usr_role,'**************')
            new_user = user_datastore.create_user(
                name = request.form['name'],
                email = request.form['email'],
                password = encrypt_password(request.form['password']),
                roles = [usr_role]
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Employee created successfully')
            return redirect(url_for('employeelist'))
        except Exception as ae:
            if(str(ae.__dict__['orig']).find("Duplicate entry")!= -1):
                flash("User with this email is already Exist!")
            else:
                flash("Failed to creata a user try again!!")
            print(ae,'####')
            logger.exception('Error in add employee',ae)
    return render_template('addmanager.html')

@app.route('/addemployee', methods=['GET','POST'])
@login_required
@roles_accepted('Manager')
def addemployee():
    roles = Role.query.all()
    print(roles)
    if request.method == "POST":
        print(request.form['name'])
        usr_role = Role.query.get(2)
        print(usr_role,'**************')
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
            print(ae,'####')
            logger.exception('Error in edit employee',ae)
            return redirect(url_for('addemployee'))
        new_employee = Employee(phone=request.form['phone'],designation=request.form['designation'],user=new_user)
        db.session.add(new_employee)
        try:
            db.session.commit()
            flash('Employee created successfully')
            return redirect(url_for('employeelist'))
        except Exception as ae:
            if(str(ae.__dict__['orig']).find("Duplicate entry")!= -1):
                flash("Employee with this phone number is already Exist!")
            else:
                flash("Failed to creata a employee try again!!")
            print(ae,'####')
            logger.exception('Error in add employee',ae)
            return redirect(url_for('addemployee'))
    return render_template('addemployee.html',roles=roles,action="create")

@app.route('/editemployee/<int:id>', methods=['GET','POST'])
@login_required
@roles_accepted('Manager')
def editemployee(id):
    user = User.query.get(id)
    cp_user = user
    print(user)
    if request.method == "POST":
        print(request.form['name'])
        try:
            usr_role = Role.query.get(2)
            print(usr_role,'**************')
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
                    flash("Failed to creata a employee try again!!")
                print(ae,'####')
                logger.exception('Error in edit employee',ae)
                return redirect(url_for('editemployee', id=id))
            emp  = Employee.query.get(user.employee.id)
            emp.phone=request.form['phone']
            emp.designation=request.form['designation']
            db.session.commit()
            flash('Employee updated successfully')
            return redirect(url_for('employeelist',))
        except Exception as ae:
            if(str(ae.__dict__['orig']).find("Duplicate entry")!= -1):
                flash("Employee with the entered phone number is already Exist!")
            else:
                flash("Failed to update a employee try again!!")
            print(ae,'####')
            logger.exception('Error in edit employee',ae)
            return redirect(url_for('editemployee', id=id))
    return render_template('addemployee.html',user=user,action="edit")

@app.route('/viewprofile/<int:id>', methods=['GET','POST'])
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

@app.route('/deleteemployee', methods=['DELETE'])
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

@app.route('/addskill', methods=['GET','POST'])
@login_required
@roles_accepted('Employee')
def addskill():
    if request.method == 'POST':
        flt = Skill.query.filter_by(name=request.form['skill'],employee=current_user.employee).first()
        print(flt,'*************')
        if flt == None:
            try:
                print(request.form,flt,'##################3')
                new_skill = Skill(
                    name=request.form['skill'],
                    percentage=int(request.form['percent']),
                    employee = current_user.employee
                )
                db.session.add(new_skill)
                db.session.commit()
                flash('Skill added successfully')
                return redirect(url_for('profile'))
            except Exception as ae:
                print(ae,'*****************')
                logger.exception('Error in add skill',ae)
                flash('Failed to add skill try again!')
        else:
            flash('Skill Already Exist!')
    return render_template('addskill.html',action="create")

@app.route('/editskill/<int:id>', methods=['GET','POST'])
@login_required
@roles_accepted('Employee')
def editskill(id):
    skill = Skill.query.get(id)
    if request.method == 'POST':
        try:
            print(request.form,'##################3')
            
            skill.name=request.form['skill']
            skill.percentage=int(request.form['percent'])
            
            db.session.commit()
            flash('Skill updated successfully')
            return redirect(url_for('profile'))
        except Exception as ae:
            print(ae,'*****************')
            flash('Failed to update try again!')
            logger.exception('Error in edit skill',ae)
    return render_template('addskill.html',skill=skill,action="edit")

@app.route('/deleteskill', methods=['DELETE'])
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

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    sk_name = []
    sk_perc = []
    for i in current_user.employee.skills:
        sk_name.append(i.name)
        sk_perc.append(i.percentage)
    return render_template('profile.html',sk_name=sk_name,sk_perc=sk_perc)

@app.route('/employee', methods=['GET','POST'])
@login_required
def employee():
    return 'employee'

if __name__=='__main__':
    app.run(debug=True)