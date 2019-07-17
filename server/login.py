import flask
from flask import jsonify
from app import app
from models import User
from flask_fas_openid import fas_login_required

from flask_fas_openid import fas_login_required, cla_plus_one_required, FAS

fas = FAS(app)

app.config['FAS_OPENID_ENDPOINT'] = 'https://id.centos.org/idp/openid/'

@app.route('/login', methods=['GET', 'POST'])
def auth_login():
    """
    Method to log into the application using FAS OpenID. 
    """
    return_point = flask.url_for("get_requests")
    if "next" in flask.request.args:
        return_point = flask.request.args["next"]
    # if flask.g.fas_user:
    if flask.session.get('FLASK_FAS_OPENID_USER'):
        return flask.redirect(return_point)
    return fas.login(return_url=return_point)

@app.route('/logout')
def auth_logout():
    """ 
    Method to log out currently logged in user from the application.
    
    """
    # if not flask.g.fas_user:
    if not flask.session.get('FLASK_FAS_OPENID_USER'):
        return jsonify({'result': 'error', 'message': 'User is already logged out.'}), 200
    
    fas.logout()
    return jsonify({'result': 'success', 'message':'You have successfully logged out'}), 200

@fas.postlogin
def set_user(return_url):
    """
    Set up user in app after FAS login.
    """
    # if flask.g.fas_user.username is None:
    if not flask.session.get('FLASK_FAS_OPENID_USER').get('username'):
        # flask.flash("Cannot go further without a username.",)
        fas.logout()
        return flask.redirect(return_url)
    
    user = flask.g.session.query(User).filter(User.username == flask.session['FLASK_FAS_OPENID_USER'].get('username'),
                                            User.email == flask.session['FLASK_FAS_OPENID_USER'].get('email')).one_or_none()
    if not user:
        new_user = User(
            username=flask.session['FLASK_FAS_OPENID_USER'].get('username'),
            email=flask.session['FLASK_FAS_OPENID_USER'].get('email'),
            gpg_key=flask.session['FLASK_FAS_OPENID_USER'].get('gpg_keyid'),
        )
        flask.g.session.add(new_user)
        flask.g.session.commit()
    # return flask.g.fas_user.username

    resp = flask.make_response(flask.redirect('http://localhost:3000/'))
    # resp.set_cookie('random cookie', 'this is the session cookie I want the browser to set for further requests')
    return resp
    # response = flask.redirect('http://localhost:3000/')
    # response.headers = {'Set-Cookie': 'this is the session cookie'}  
    # return response

@app.route('/logged_in')
@fas_login_required
def random():
    return 'hey, you can see me if youre logged in'