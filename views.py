import flask
from flask import render_template, request
from app import app
from models import *
from flask_fas_openid import fas_login_required

@app.route('/')
def index():
    return render_template('home_page.html', user=flask.g.fas_user)

@app.route('/requests', methods=['GET', 'POST'])
@fas_login_required
def requests():
        if request.method == 'POST':
            '''Create a new project request'''
            new_request = Request(**request.args)
            flask.g.session.add(new_request)
            flask.g.session.commit()
            return render_template('request_created.html', request=new_request.request_id)

        requests = flask.g.session.query(Request).all()
        return render_template('requests.html', requests=requests, user=flask.g.fas_user)

@app.route('/projects')
def projects(): 
        projects = flask.g.session.query(Request).all()
        return render_template('projects.html', projects=projects, user=flask.g.fas_user)


