# coding: utf-8
import json
from jieba import analyse
from flask import render_template, Blueprint, flash, redirect, url_for, abort, request
from werkzeug.contrib.atom import AtomFeed
from ..models import db, Blog, Post, ApprovementLog
from ..forms import AddBlogForm

bp = Blueprint('blog', __name__)


@bp.route('/<int:uid>', defaults={'page': 1})
@bp.route('/<int:uid>/page/<int:page>')
def view(uid, page):
    blog = Blog.query.get_or_404(uid)
    if not blog.is_approved:
        abort(404)
    posts_count = blog.posts.filter(~Post.hide).count()
    posts = blog.posts.filter(~Post.hide). \
        order_by(Post.published_at.desc(), Post.updated_at.desc()).paginate(page, 20)
    return render_template('blog/view.html', blog=blog, posts=posts, posts_count=posts_count)


@bp.route('/all')
def all_blogs():
    blogs = Blog.query.filter(Blog.is_approved)
    return render_template('blog/all_blogs.html', blogs=blogs)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    """推荐博客"""
    form = AddBlogForm()
    if form.validate_on_submit():
        blog = Blog(**form.data)
        db.session.add(blog)
        log = ApprovementLog(blog=blog)  # 添加log
        db.session.add(log)
        db.session.commit()
        flash('非常感谢你的推荐！我们会在第一时间审核。')
        return redirect(url_for('site.approve_results'))
    return render_template('blog/add.html', form=form)


@bp.route('/post/<int:uid>/redirect')
def redirect_post(uid):
    post = Post.query.get_or_404(uid)
    if not post.clicks:
        post.clicks = 0
    post.clicks += 1
    db.session.add(post)
    db.session.commit()
    return redirect(post.url)


@bp.route('/post/<int:uid>')
def post(uid):
    post = Post.query.get_or_404(uid)
    if post.blog.is_protected or not post.blog.is_approved:
        abort(404)
    if post.hide:
        abort(404)
    if post.content:
        keywords = analyse.extract_tags(post.content, topK=20, withWeight=True)
        tags = [{'text': tag, 'weight': weight} for tag, weight in keywords]
    else:
        tags = []
    return render_template('blog/post.html', post=post, tags=json.dumps(tags))


@bp.route('/<int:uid>/feed')
def feed(uid):
    blog = Blog.query.get_or_404(uid)
    if not blog.is_approved and not blog.for_special_purpose:
        abort(404)
    if blog.feed:
        abort(404)

    feed = AtomFeed(blog.title, feed_url=request.url, url=blog.url, id=blog.url)
    if blog.subtitle:
        feed.subtitle = blog.subtitle
    for post in blog.posts.filter(~Post.hide). \
            order_by(Post.published_at.desc(), Post.updated_at.desc()).limit(15):
        updated = post.updated_at if post.updated_at else post.published_at
        feed.add(post.title, post.content, content_type='html', author=blog.author,
                 url=post.url, id=post.url, updated=updated)
    response = feed.get_response()
    response.headers['Content-Type'] = 'application/xml'
    return response


@bp.route('/posts', defaults={'page': 1})
@bp.route('/posts/page/<int:page>')
def posts(page):
    posts = Post.query. \
        filter(~Post.hide).filter(Post.blog.has(Blog.is_approved)). \
        order_by(Post.published_at.desc(), Post.updated_at.desc()). \
        paginate(page, 20)
    return render_template('blog/posts.html', posts=posts)
