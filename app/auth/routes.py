from app.auth import auth_bp
from app.auth.auth_functions import basic_auth
from flask import request
from app.models import Role, User
from werkzeug.security import generate_password_hash
from flask_login import logout_user
from app import db
from to_do_restful_api import create_response


@auth_bp.route('/signup', methods=['POST'])
def signup():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    username = request.form.get('username')
    password = request.form.get('password')
    role_name = request.form.get('role')

    user = User.query.filter_by(username=username).first()
    role_instance = Role.query.filter_by(name=role_name).first()

    if user:
        return create_response(False, "Username already exists.")

    if not role_instance:
        return create_response(False, "The role is not valid.")

    new_user = User(first_name=first_name, last_name=last_name, username=username,
                    password_hash=generate_password_hash(password, method='sha256'), user_role=role_instance)
    db.session.add(new_user)
    db.session.commit()

    return create_response(True, "User created.")


@auth_bp.route('/login', methods=['POST'])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    db.session.commit()
    return create_response(True, "User successfully logged in.", {
        "first_name": user.first_name, "last_name": user.last_name, "role": user.user_role.name, 'token': token
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return create_response(True, "User logged out.")
