import flask
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
    return_point = flask.url_for("requests")
    if "next" in flask.request.args:
        return_point = flask.request.args["next"]
    print('RETURN POINT-------------------',return_point)
    if flask.g.fas_user:
        return flask.redirect(return_point)
    return fas.login(return_url=return_point)

@app.route('/logout')
def auth_logout():
    """ 
    Method to log out currently logged in user from the application.
    
    """
    print('-------------------logging out-------------------')
    return_point = flask.url_for("requests")
    if "next" in flask.request.args:
        return_point = flask.request.args["next"]

    if not flask.g.fas_user:
        return flask.redirect(return_point)

    fas.logout()
    return flask.redirect(return_point)

@fas.postlogin
def set_user(return_url):
    """
    Set up user in app after FAS login.
    """
    print('postlogin', return_url)
    if flask.g.fas_user.username is None:
        # flask.flash("Cannot go further without a username.",)
        fas.logout()
        return flask.redirect(return_url)
    
    user = flask.g.session.query(User).filter(User.username == flask.g.fas_user.username,
                                            User.email == flask.g.fas_user.email).one_or_none()
    if not user:
        new_user = User(
            username=flask.g.fas_user.username,
            email=flask.g.fas_user.email,
            gpg_key=flask.g.fas_user.gpg_keyid,
        )
        flask.g.session.add(new_user)
        flask.g.session.commit()
    # return flask.redirect(return_url)
    return flask.g.fas_user.username


@app.route('/logged_in')
@fas_login_required
def random():
    return 'hey, you can see me if youre logged in'