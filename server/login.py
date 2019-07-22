import flask
from flask import jsonify
from app import app
from models import User
from flask_fas_openid import FAS


fas = FAS(app)

app.config['FAS_OPENID_ENDPOINT'] = 'https://id.centos.org/idp/openid/'

@app.route('/login', methods=['GET', 'POST'])
def auth_login():
    """
    Method to log into the application using FAS OpenID. 
    """
    if flask.session.get('FLASK_FAS_OPENID_USER'):
        return 'http://localhost:3000/projects/'
    return fas.login()

@app.route('/logout')
def auth_logout():
    """ 
    Method to log out currently logged in user from the application.
    
    """
    if not flask.session.get('FLASK_FAS_OPENID_USER'):
        return jsonify({'result': 'error', 'message': 'User is already logged out.'}), 200
    
    fas.logout()
    return jsonify({'result': 'success', 'message':'You have successfully logged out'}), 200

@fas.postlogin
def set_user(return_url):
    """
    Set up user in app after FAS login.
    """
    if not flask.session.get('FLASK_FAS_OPENID_USER').get('username'):
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

    resp = flask.make_response(flask.redirect('http://localhost:3000/'))
    return resp
