# coding: utf-8
from flask import render_template, Blueprint
from ..models import db, Blog, Post, ApprovementLog

bp = Blueprint('site', __name__)


@bp.route('/page', defaults={'page': 1})
@bp.route('/page/<int:page>')
def index(page):
    """首页"""
    recommend_posts = Post.query.filter(Post.recommend). \
        order_by(Post.published_at.desc(), Post.updated_at.desc()).paginate(page, 10)

    blogs_query = Blog.query.filter(Blog.is_approved)
    blogs_count = blogs_query.count()
    latest_blogs = blogs_query.order_by(Blog.created_at.desc()).limit(20)

    posts_query = Post.query.filter(~Post.hide). \
        filter(Post.blog.has(Blog.is_approved))
    posts_count = posts_query.count()
    latest_posts = posts_query.order_by(Post.published_at.desc(), Post.updated_at.desc()).limit(20)
    return render_template('site/index.html', latest_posts=latest_posts,
                           latest_blogs=latest_blogs, blogs_count=blogs_count,
                           posts_count=posts_count, recommend_posts=recommend_posts)


@bp.route('/approve_results', defaults={'page': 1})
@bp.route('/approve_results/page/<int:page>')
def approve_results(page):
    logs = ApprovementLog.query
    unprocessed_logs = logs.filter(ApprovementLog.status == -1).order_by(
        ApprovementLog.updated_at.desc())
    processed_logs = logs.filter(ApprovementLog.status != -1).order_by(
        ApprovementLog.status.desc(),
        ApprovementLog.updated_at.desc()).paginate(page, 20)
    return render_template('site/approve_results.html', unprocessed_logs=unprocessed_logs,
                           processed_logs=processed_logs)


@bp.route('/suggest')
def suggest():
    return render_template('site/suggest.html')


@bp.route('/about')
def about():
    """关于页"""
    return render_template('site/about.html')
