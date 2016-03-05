# -*- coding: UTF-8 -*-
from flask import jsonify

from . import api
from ..exceptions import ValidationError


def forbidden(messages):
    response = jsonify({'errors': 'not found.', 'messages': messages})
    response.status_code = 403
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
