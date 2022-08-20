from app.tasks import tasks_bp
from app.auth.auth_functions import token_auth, basic_auth
from flask import request
from app.models import User, Project, Task
from app import db
from to_do_restful_api import create_response, db_session_data


@tasks_bp.route('/insert_project', methods=['POST'])
@token_auth.login_required
def insert_project():
    if basic_auth.current_user().user_role.name != "manager":
        return create_response(False, "Access is denied.")

    project_name = request.form.get('project_name')

    project_with_same_name = Project.query.filter_by(
        project_name=project_name).first()
    if project_with_same_name:
        return create_response(False, "Project name " + project_name + " already exists.")

    new_project = Project(project_name=project_name)
    db.session.add(new_project)
    db.session.commit()

    return create_response(True, "The new project is created successfully.")


@tasks_bp.route('/insert_task', methods=['POST'])
@token_auth.login_required
def insert_task():
    if basic_auth.current_user().user_role.name != "manager":
        return create_response(False, "Access is denied.")

    project_name = request.form.get('project_name')
    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description')

    project = Project.query.filter_by(project_name=project_name).first()
    if not project:
        return create_response(False, "Project " + project_name + " does not exists.")

    new_task = Task(task_name=task_name,
                    task_description=task_description, project_id=project.id)
    db.session.add(new_task)
    db.session.commit()

    return create_response(True, "The new task is created successfully.")


@tasks_bp.route('/assign_task', methods=['POST'])
@token_auth.login_required
def assign_task():
    if basic_auth.current_user().user_role.name != "manager":
        return create_response(False, "Access is denied.")

    task_id = request.form.get('task_id')
    username = request.form.get('username')

    task_to_be_updated = Task.query.filter_by(id=task_id).first()
    if not task_to_be_updated:
        return create_response(False, "The task does not exists.")
    user = User.query.filter_by(username=username).first()
    if not user:
        return create_response(False, "User " + username + " does not exists.")

    task_to_be_updated.users.append(user)
    db.session.add(task_to_be_updated)
    db.session.commit()

    return create_response(True, "The task is assigned to the user.")


@tasks_bp.route('/revoke_assign_task', methods=['POST'])
@token_auth.login_required
def revoke_assign_task():
    if basic_auth.current_user().user_role.name != "manager":
        return create_response(False, "Access is denied.")

    task_id = request.form.get('task_id')
    username = request.form.get('username')

    task_to_be_updated = Task.query.filter_by(id=task_id).first()
    if not task_to_be_updated:
        return create_response(False, "The task does not exists.")
    user = User.query.filter_by(username=username).first()
    if not user:
        return create_response(False, "User " + username + " does not exists.")

    task_to_be_updated.users.remove(user)
    db.session.add(task_to_be_updated)
    db.session.commit()

    return create_response(True, "The task assignment to the user is revoked.")


@tasks_bp.route('/update_task', methods=['POST'])
@token_auth.login_required
def update_task():
    task_id = request.form.get('task_id')
    project_name = request.form.get('project_name')
    new_task_name = request.form.get('task_name')
    new_task_description = request.form.get('task_description')

    task_to_be_updated = Task.query.filter_by(id=task_id).first()
    if not task_to_be_updated:
        return create_response(False, "The task does not exists.")

    project = Project.query.filter_by(project_name=project_name).first()
    if not project:
        return create_response(False, "Project " + project_name + " does not exists.")

    if basic_auth.current_user().user_role.name != "manager" and not Task.query.join(Task.users).filter_by(
        id=task_id, username=basic_auth.current_user().username
    ).first():
        return create_response(False, "Access is denied.")

    task_to_be_updated.task_name = new_task_name
    task_to_be_updated.task_description = new_task_description
    task_to_be_updated.project_id = project.id

    db.session.add(task_to_be_updated)
    db.session.commit()

    return create_response(True, "The task is updated successfully.")


@tasks_bp.route('/delete_task', methods=['POST'])
@token_auth.login_required
def delete_task():
    task_id = request.form.get('task_id')

    task_to_be_updated = Task.query.filter_by(id=task_id)
    if task_to_be_updated.count() == 0:
        return create_response(False, "The task does not exists.")

    if basic_auth.current_user().user_role.name != "manager" and not Task.query.join(Task.users).filter_by(
        id=task_id, username=basic_auth.current_user().username
    ).first():
        return create_response(False, "Access is denied.")

    task_to_be_updated.delete()
    db.session.commit()

    return create_response(True, "The task is deleted successfully.")


@tasks_bp.route('/get_task_list_by_user', methods=['POST'])
@token_auth.login_required
def get_task_list_by_user():
    username = request.form.get('username')
    user = None if not username else User.query.filter_by(
        username=username).first()
    if not user:
        return create_response(False, "User not found.")

    report_query = db_session_data.db_session.query(Task).join((User, Task.users)).filter(User.username == username)

    size_of_list = report_query.count()
    task_list = []
    for each_task in report_query.all():
        task_list.append({"task_id": each_task.id, "task_name": each_task.task_name, "task_description": each_task.task_description})

    return create_response(True, "The user tasks are listed.", {"size_of_list": size_of_list, "task_list": task_list})


@tasks_bp.route('/get_task_list_by_project', methods=['POST'])
@token_auth.login_required
def get_task_list_by_project():
    project_name = request.form.get('project_name')
    project_id = Project.query.filter_by(project_name=project_name).first().id

    report_query = Task.query.filter_by(project_id=project_id)
    size_of_list = report_query.count()
    task_list = []
    for each_task in report_query.all():
        task_list.append({"task_id": each_task.id, "task_name": each_task.task_name,
                         "task_description": each_task.task_description, "project_id": each_task.project_id})

    return create_response(True, "The user tasks listed.", {"size_of_list": size_of_list, "project_name": project_name, "task_list": task_list})
