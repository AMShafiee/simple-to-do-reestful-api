from datetime import datetime, timedelta
from app import db, login
import base64
import os
from flask_login import UserMixin
from sqlalchemy import event

task_assignment = db.Table('task_assignment',
                           db.Column('user_id', db.Integer,
                                     db.ForeignKey('user.id')),
                           db.Column('task_id', db.Integer,
                                     db.ForeignKey('task.id'))
                           )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=False, unique=False)
    last_name = db.Column(db.String(30), index=False, unique=False)
    username = db.Column(db.String(30), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    tasks = db.relationship("Task", secondary=task_assignment,
                            primaryjoin=lambda: User.id == task_assignment.c.user_id,
                            secondaryjoin=lambda: Task.id == task_assignment.c.task_id,
                            backref="users")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='user_role', lazy='dynamic')


@event.listens_for(Role.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(Role(name='developer'))
    db.session.add(Role(name='manager'))
    db.session.commit()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(30), unique=True)
    tasks = db.relationship(
        'Task', backref='related_project', lazy='dynamic')

    def __repr__(self):
        return '<Project {}>'.format(self.project_name)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(30))
    task_description = db.Column(db.String(100))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return '<Task {}>'.format(self.task_name)
