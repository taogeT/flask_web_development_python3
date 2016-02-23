# -*- coding: UTF-8 -*-
from datetime import datetime
from flask import render_template, session, flash, redirect, url_for, current_app

from . import main
from .forms import NameForm
from ..models import User
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name and old_name != form.name.data:
            flash('Looks like you change your name!')
        user = User.query.filter_by(username=form.name.data).first()
        if user:
            session['known'] = True
        else:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                pass
                # send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                #            'mail/new_user', user=user)
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', current_time=datetime.utcnow(),
                           name=session.get('name'), form=form,
                           known=session.get('known'))


@main.route('/user')
@main.route('/user/<name>')
def user(name=''):
    return render_template('user.html', name=name)
