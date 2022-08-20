from app import create_app, db
from flask import jsonify, make_response


class db_session_data:
    db_session = None


def create_response(was_successful, message, data={}):
    response = make_response(
        jsonify(
            {"was_successful": was_successful, "message": message, "data": data}
        ),
    )
    response.headers["Content-Type"] = "application/json"
    return response


to_do_restful_app, db_session = create_app()
db_session_data.db_session = db.session
