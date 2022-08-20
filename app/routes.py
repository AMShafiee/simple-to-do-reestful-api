from app import flask_object
from flask_login import login_required 
from models import User
from flask import render_template

@flask_object.route('/')
@flask_object.route('/index')
def index():
    return "Hello, World!"


@flask_object.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)
