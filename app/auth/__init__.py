from flask import Blueprint

auth_bp = Blueprint('authentication', __name__)

from app.auth import routes
# from app.errors import handlers  --> I import the handlers.py module, so that the error handlers in it are registered with the blueprint.