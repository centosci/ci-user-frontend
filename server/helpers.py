import flask
from models import *

def add_comment(request_id, user_id, comment):
    """
    Add comment on a project request.
    """
    
    new_comment = Comment(user_id=user_id, request_id=request_id, comment=comment)
    flask.g.session.add(new_comment)
    return {'result': 'success', 'message': 'Comment added successfully.'}

def create_project_for_request(req, user):
    """
    Add a new project for request
    """
    new_project = Project(project_name=req.project_name, description=req.project_desc)
    flask.g.session.add(new_project)

    # new_member = ProjectMember(project_id=str(new_project.id), user_id=str(user.id))
    # flask.g.session.add(new_member)

    return {'result': 'success', 'message': 'Successfully reated new project.'}

def add_member_to_project(req, user):
    """
    Add user to existing project
    """
    project = flask.g.session.query(Project).filter(Project.project_name==req.project_name).one_or_none()
    if not project:
        return {'result': 'error', 'message': 'Project not found.'}
    
    new_member = ProjectMember(project_id=str(project.id), user_id=str(user.id))
    flask.g.session.add(new_member)

    return {'result': 'success', 'message': 'Successfully reated new project.'}
