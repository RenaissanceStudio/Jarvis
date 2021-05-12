from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from .errors import forbidden, unauthorized

from . import api
from ..model import User

auth = HTTPBasicAuth()


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@auth.verify_password
def verify_password(email, password):
    if email == '':
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user:
        return forbidden('Unauthorized user')
