# -*- coding: UTF-8 -*-
from flask import g, jsonify
from flask.ext.httpauth import HTTPBasicAuth

from ..models import AnonymousUser, User
from .errors import forbidden, unauthorized
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if not email_or_token:
        g.current_user = AnonymousUser()
        return True
    if not password:
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).one()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    if g.current_user.is_anonymous or not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@api.route('/token/')
@auth.login_required
def token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token().decode('utf-8'),
                    'expiration': 3600})
