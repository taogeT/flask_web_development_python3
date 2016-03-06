# -*- coding: UTF-8 -*-
from flask import jsonify, url_for, request, g, current_app

from ..models import Post, Permission
from . import api
from .. import db
from .decorators import permission_required
from .errors import forbidden


@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
                    page=page,
                    per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)
    posts = pagination.items
    page_next = url_for('.get_posts', page=page+1, _external=True) if pagination.has_next else None
    page_prev = url_for('.get_posts', page=page-1, _external=True) if pagination.has_prev else None
    return jsonify({'posts': [post.to_json() for post in posts],
                    'next': page_next, 'prev': page_prev,
                    'count': pagination.total})


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit() #ID
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('.get_post', id=post.id, _external=True)}


@api.route('/post/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/post/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post():
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())
