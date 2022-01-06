from flask import Flask
from flask_security import SQLAlchemyUserDatastore
from datetime import datetime
from flask_security.utils import encrypt_password
from flask_sqlalchemy import SQLAlchemy
from main import app, db
from flask_user import UserManager


user_manager = UserManager(app, db, User)

class User(db.Model, UserMixin):
	__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
	email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
	roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
user1 = User(username='admin', email='user007@example.com', active=True,
             password=user_manager.hash_password('admin'))
user.roles.append('Admin')
db.session.add(user)
db.session.commit()
db.session.refresh(user)