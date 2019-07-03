import flask
from flask import render_template, request, redirect
from app import app
from models import *
from flask_fas_openid import fas_login_required

@app.route('/')
def index():
    return render_template('home_page.html', user=flask.g.fas_user)

@app.route('/request/new', methods=['GET', 'POST'])
@fas_login_required
def create_new_request():
    if request.method == 'POST':
        '''Create a new project request'''
        project_name = request.form['project_name']
        project_desc = request.form['project_desc']
        gpg_key = request.form['gpg_key']
        
        if not project_name or not project_desc:
            return render_template('create_request.html', user=flask.g.fas_user, alert='Please provide input for Project details')
        
        user = flask.g.session.query(User).filter(User.email == flask.g.fas_user.email).one_or_none()

        if not gpg_key and not user.gpg_key:
            return render_template('create_request.html', user=flask.g.fas_user, alert='Please add input for GPG Key')

        if gpg_key:
            user.gpg_key = gpg_key

        request_exists = flask.g.session.query(Request).filter(Request.project_name == project_name).one_or_none()
        if request_exists:
            return render_template('create_request.html', user=flask.g.fas_user, alert=f'Request for this project already exists! Please refer to Request ID: {request_exists.id}')

        new_request = Request(user_id=str(user.id), project_name=project_name, project_desc=project_desc)
        flask.g.session.add(new_request)
            
        flask.g.session.commit()
        
        return render_template('create_request.html', user=flask.g.fas_user, success=new_request.id)

    return render_template('create_request.html', user=flask.g.fas_user)

@app.route('/requests', methods=['GET'])
@fas_login_required
def get_requests():
    print(flask.request.endpoint)
    all_requests = flask.g.session.query(Request, User.username).join(User, Request.user_id == User.id).all()
    requests = []
    for request, requested_by in all_requests:
        request_obj = request.__dict__
        request_obj['username'] = requested_by
        requests.append(request_obj)
    return render_template('requests.html', requests=requests, user=flask.g.fas_user)

@app.route('/request/<string:request_id>', methods=['GET'])
@fas_login_required
def get_individual_request(request_id):
    current_req = flask.g.session.query(Request).filter(Request.id == request_id).one_or_none()
    comments = flask.g.session.query(Comment).filter(Comment.request_id == request_id).all()
    return render_template('individual_request.html', current_req=current_req, comments=comments, user=flask.g.fas_user)

@app.route('/projects')
def projects(): 
    projects = flask.g.session.query(Request).all()
    return render_template('projects.html', projects=projects, user=flask.g.fas_user)


