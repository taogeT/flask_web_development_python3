# -*- coding: UTF-8 -*-
from threading import Thread
from flask import render_template, current_app
from flask.ext.mail import Message

from . import mail


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(subject=current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to],
                  body=render_template(template + '.txt', **kwargs),
                  html=render_template(template + '.html', **kwargs))
    thr = Thread(target=send_async_mail, kwargs={'app': current_app, 'msg': msg})
    thr.start()
    return thr
