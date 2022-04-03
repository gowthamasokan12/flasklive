from flask_security import UserMixin, RoleMixin
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from extensions import *


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

