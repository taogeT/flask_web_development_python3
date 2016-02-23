# -*- coding: UTF-8 -*-
from threading import Thread
from flask import render_template
from flask.ext.mail import Message

from . import mail
from manager import app


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to],
                  body=render_template(template + '.txt', **kwargs),
                  html=render_template(template + '.html', **kwargs))
    thr = Thread(target=send_async_mail, app=app, msg=msg)
    thr.start()
    return thr
