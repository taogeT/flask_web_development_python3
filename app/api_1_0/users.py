# -*- coding: UTF-8 -*-
from flask import jsonify, current_app, url_for, request

from . import api
from ..models import User, Post


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
                    page=page,
                    per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)
    posts = pagination.items
    page_next = url_for('.get_user_posts', page=page+1, _external=True) if pagination.has_next else None
    page_prev = url_for('.get_user_posts', page=page-1, _external=True) if pagination.has_prev else None
    return jsonify({'posts': [post.to_json() for post in posts],
                    'next': page_next, 'prev': page_prev,
                    'count': pagination.total})


@api.route('/users/<int:id>/timeline/')
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts().order_by(Post.timestamp.desc()).paginate(
                    page=page,
                    per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)
    posts = pagination.items
    page_next = url_for('.get_user_followed_posts', page=page+1, _external=True) if pagination.has_next else None
    page_prev = url_for('.get_user_followed_posts', page=page-1, _external=True) if pagination.has_prev else None
    return jsonify({'posts': [post.to_json() for post in posts],
                    'next': page_next, 'prev': page_prev,
                    'count': pagination.total})
