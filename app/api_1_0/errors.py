# -*- coding: UTF-8 -*-
from flask import jsonify

from . import api
from ..exceptions import ValidationError


def forbidden(messages):
    response = jsonify({'errors': 'forbidden', 'messages': messages})
    response.status_code = 403
    return response


def bad_request(messages):
    response = jsonify({'errors': 'bad request', 'messages': messages})
    response.status_code = 401
    return response


def unauthorized(messages):
    response = jsonify({'errors': 'unauthorized', 'messages': messages})
    response.status_code = 400
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
