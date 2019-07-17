import flask
from flask import jsonify, request
import datetime
from app import app
from models import *
from flask_fas_openid import fas_login_required
from helpers import add_comment, create_project_for_request, add_member_to_project

@app.route('/')
def index():
    return 'Im the flask app home page'


@app.route('/user')
@fas_login_required
def get_user():

    '''Get user data from database'''

    user_record = flask.g.session.query(User).filter(User.email == flask.session['FLASK_FAS_OPENID_USER']['email']).one_or_none()
    row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
    user = row2dict(user_record)
    return jsonify(user), 200


@app.route('/new-request', methods=['POST'])
@fas_login_required
def create_new_request():

    '''Create a new project request'''

    project_name = request.form.get('project_name')
    project_desc = request.form.get('project_desc')
    gpg_key = request.form.get('gpg_key')
    new_project = False if request.form.get('new_project') and request.form['new_project'] != 'true' else True

    if not project_name or (new_project and not project_desc):
        return jsonify({'result': 'error', 'message':'Please provide input for Project details'}), 200
    if not gpg_key:
        return jsonify({'result': 'error', 'message':'Please add input for GPG Key'}), 200

    user = flask.g.session.query(User).filter(User.email == flask.g.fas_user.email).one_or_none()

    if gpg_key != user.gpg_key:
        user.gpg_key = gpg_key

    request_exists = flask.g.session.query(Request).filter(Request.project_name == project_name).one_or_none()
    if request_exists:
        return jsonify({'result': 'error', 'message':f'Request for this project already exists! Please refer to Request ID: {request_exists.id}'}), 200

    new_request = Request(user_id=str(user.id), project_name=project_name, project_desc=project_desc)
    flask.g.session.add(new_request)
        
    flask.g.session.commit()
    
    return jsonify({'result': 'success', 'message': 'Request created succesfully!'}), 200


@app.route('/requests', methods=['GET'])
@fas_login_required
def get_requests():

    '''Get all project requests'''

    all_requests = flask.g.session.query(Request, User.username
        ).join(User, Request.user_id == User.id
        ).all()

    requests = []
    row2dict = lambda r: {
        c.name: str(getattr(r, c.name)) 
        for c in r.__table__.columns 
        if c.name in ['id', 'project_name', 'status', 'project_desc' ]
        }
    
    for request, requested_by in all_requests:
        request_obj = row2dict(request)
        request_obj['requested_by'] = requested_by
        requests.append(request_obj)

    return jsonify(requests=requests), 200


@app.route('/requests/<string:request_id>', methods=['GET'])
@fas_login_required
def get_individual_request(request_id):

    '''Get individual request data'''

    current_request, requested_by = flask.g.session.query(Request, User.username
        ).join(User, Request.user_id == User.id
        ).filter(Request.id == request_id
        ).one_or_none()

    row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
    
    current_request_dict = row2dict(current_request)
    current_request_dict['requested_by'] = requested_by

    comments = flask.g.session.query(Comment, User
        ).join(User, User.id == Comment.user_id
        ).filter(Comment.request_id == request_id
        ).order_by(Comment.updated_at
        ).all()

    comments_list = []
    for comment, commented_by in comments:
        comments_dict = row2dict(comment)
        comments_dict['commented_by'] = commented_by.username
        comments_list.append(comments_dict)

    return jsonify({'current_request': current_request_dict, 'comments': comments_list}), 200


@app.route('/edit-request/', methods=['POST'])
@fas_login_required
def edit_request():

    '''
    Allow user to cancel his own request.
    Allow users with admin or superuser roles to approve or reject request.
    '''

    action = request.args.get('action')
    request_id = request.args.get('request_id')

    user = flask.session['FLASK_FAS_OPENID_USER'].get('username')
    user_obj = flask.g.session.query(User).filter(User.username == user).one_or_none()

    current_request, requested_by = flask.g.session.query(Request, User.username
        ).join(User, Request.user_id == User.id
        ).filter(
            Request.id == request_id,
            Request.status == 'pending',
        ).one_or_none()

    if not current_request:
        return jsonify({'result': 'error', 'message': 'Cannot find valid request.'}), 200

    if (user != requested_by and user_obj.role not in ['admin', 'superuser'] and action == 'declined') or \
        (user_obj.role not in ['admin', 'superuser'] and action == 'approved'):
        return jsonify({'result': 'error', 'message': 'User does not have permission to perform this action.'}), 200

    current_request.status = action
    current_request.updated_by = user
    current_request.updated_at = datetime.datetime.utcnow()

    action_response = {}
    if action == 'approved':
        if current_request.project_desc:
            action_response = create_project_for_request(current_request, user_obj)
        else:
            action_response = add_member_to_project(current_request, user_obj)

    elif action == 'declined':
        if user != requested_by:
            comment = request.args.get('reject_reason')
            action_response = add_comment(request_id, str(user_obj.id), comment)
        else:
            action_response = {'result': 'success'}
    
    if action_response.get('result') != 'success':
        return jsonify({'result': 'error', 'message': 'Something went wrong!'})

    flask.g.session.commit()
    return jsonify({'result': 'success', 'message': f'{action} action completed for request.'}), 200
        

@app.route('/comment', methods=['POST'])
@fas_login_required
def post_comment():

    '''Add comment on a request'''

    request_id = request.form.get('request_id')
    comment = request.form.get('comment')
    user = flask.session['FLASK_FAS_OPENID_USER']['username']
    user_obj = flask.g.session.query(User).filter(User.username == user).one_or_none()
    
    response = add_comment(request_id, str(user_obj.id), comment)
    if response['result'] == 'success':
        flask.g.session.commit()
        return jsonify({'result': 'success', 'message': response['message']})


@app.route('/projects')
def projects():

    '''Get all projects'''

    all_projects = flask.g.session.query(Project).all()

    projects = []
    row2dict = lambda r: {
        c.name: str(getattr(r, c.name)) 
        for c in r.__table__.columns 
        if c.name in ['id', 'project_name', 'description', 'description', 'created_at']
        }
    
    for project in all_projects:
        project_obj = row2dict(project)
        projects.append(project_obj)

    return jsonify(projects=projects), 200
