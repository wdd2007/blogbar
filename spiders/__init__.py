# coding: utf-8
from application.models import db, Blog, Post
from application.utils.blog import check_offline
from .lifesinger import LifeSingerSpider
from .wangyin import WangYinSpider
from .livid import LividSpider
from .fouber import FouberSpider
from .meizhi import MeiZhiSpider


spiders = [
    LifeSingerSpider,
    WangYinSpider,
    LividSpider,
    FouberSpider,
    MeiZhiSpider
]


def grab_by_spider(spider_class):
    new_posts_count = 0
    blog = Blog.query.filter(Blog.url == spider_class.url).first()

    # 若blog不存在，则创建
    if not blog:
        blog = Blog(url=spider_class.url, title=spider_class.title, is_approved=True,
                    subtitle=spider_class.subtitle, author=spider_class.author, has_spider=True)
        if spider_class.for_special_purpose:  # 特殊用途
            blog.is_approved = False
            blog.for_special_purpose = True
        db.session.add(blog)
        db.session.commit()

    # 检测博客是否在线
    blog.offline = check_offline(blog.url)

    for p in spider_class.get_posts_():
        url = p['url']
        title = p['title']
        published_at = p['published_at']

        post = Post.query.filter(Post.url == url).first()

        # 新文章
        if not post:
            new_posts_count += 1
            content = spider_class.get_post_(url)
            post = Post(url=url, title=title, published_at=published_at, content=content)
            blog.posts.append(post)
            print(" new - %s" % title)
        elif published_at != post.published_at:  # 更新文章
            post.title = title
            post.published_at = published_at
            post.content = spider_class.get_post_(url)
            db.session.add(post)
            print(" update - %s" % title)
    db.session.add(blog)
    db.session.commit()
    return new_posts_count
