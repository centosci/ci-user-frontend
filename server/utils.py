import flask
import sqlalchemy
from functools import wraps
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

import string
import random

BASE = declarative_base()
SESSIONMAKER = None

def set_request():
    """ 
    Preparing every request.
    """
    # flask.session.permanent = True  
    if not hasattr(flask.g, "session") or not flask.g.session:
        flask.g.session = create_session(flask.current_app.config["SQLALCHEMY_DATABASE_URI"])

    # flask.g.nonce = "".join(random.choice(string.ascii_letters + string.digits) for x in range(25))

def end_request(exception=None):
    """
    Remove the DB session at the end of each request.
    """
    flask.g.session.remove()

def create_session(db_url=None, debug=False, pool_recycle=3600):
    """ 
    Create the Session object to use to query the database.
    """
    global SESSIONMAKER

    if SESSIONMAKER is None or db_url != f'{SESSIONMAKER.kw["bind"].engine.url}':
        engine = sqlalchemy.create_engine(
            db_url,
            echo=debug,
            pool_recycle=pool_recycle,
            client_encoding="utf8",
        )
        SESSIONMAKER = sessionmaker(bind=engine)

    scopedsession = scoped_session(SESSIONMAKER)
    BASE.metadata.bind = scopedsession
    return scopedsession