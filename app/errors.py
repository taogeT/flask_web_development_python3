# -*- coding: UTF-8 -*-
from flask import render_template

from manager import app


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
