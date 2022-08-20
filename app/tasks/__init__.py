from flask import Blueprint

tasks_bp = Blueprint('tasks', __name__)

from app.tasks import routes
# from app.errors import handlers  --> I import the handlers.py module, so that the error handlers in it are registered with the blueprint.