# -*- coding: UTF-8 -*-
from flask import jsonify, request, url_for, g, current_app

from . import api
from .decorators import permission_required
from ..models import Post, Permission, Comment
from .. import db


@api.route('/post/<int:id>/comments/')
def get_post_comments(id):
    post = Post.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.paginate(
                    page=page,
                    per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
                    error_out=False)
    comments = pagination.items
    page_next = url_for('.get_post_comments', page=page+1, _external=True) if pagination.has_next else None
    page_prev = url_for('.get_post_comments', page=page-1, _external=True) if pagination.has_prev else None
    return jsonify({'comments': [comment.to_json() for comment in comments],
                    'next': page_next, 'prev': page_prev,
                    'count': pagination.total})


@api.route('/post/<int:id>/comments/')
@permission_required(Permission.COMMENT)
def new_post_comments(id):
    post = Post.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.post = post
    comment.author = g.current_user
    db.session.add(comment)
    return jsonify(comment.to_json()), 201, \
        {'Location': url_for('.get_comment', id=comment.id, _external=True)}


@api.route('/comments/')
def get_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.paginate(
                    page=page,
                    per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
                    error_out=False)
    comments = pagination.items
    page_next = url_for('.get_comments', page=page+1, _external=True) if pagination.has_next else None
    page_prev = url_for('.get_comments', page=page-1, _external=True) if pagination.has_prev else None
    return jsonify({'comments': [comment.to_json() for comment in comments],
                    'next': page_next, 'prev': page_prev,
                    'count': pagination.total})


@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())
