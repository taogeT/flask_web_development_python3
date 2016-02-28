# -*- coding: UTF-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flask import abort, current_app
from flask.ext.login import login_required, current_user

from . import main
from .forms import PostForm, UserEditProfileForm, AdminEditProfileForm
from ..models import User, Permission, Role, Post
from .. import db
from ..decorators import permission_required, admin_required


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
                page=page,
                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
    return render_template('index.html', pagination=pagination, form=form)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    page = request.args.get('page', type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
                page=page,
                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
    return render_template('user.html', user=user, pagination=pagination)


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderates_only():
    return "For moderators!"


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UserEditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = AdminEditProfileForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('User\'s profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
