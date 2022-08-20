from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from to_do_restful_api import create_response
from werkzeug.security import check_password_hash


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user or check_password_hash(user.password_hash, password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return create_response(False, "Username/password is invalid.")


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return create_response(False, "Token is invalid.")
