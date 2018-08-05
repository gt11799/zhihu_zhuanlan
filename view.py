#! coding:utf-8
import time
from flask import request, url_for, redirect, Blueprint, jsonify

from model import Wujun


bp = Blueprint("main", __name__, url_prefix=None)


@bp.route("/", methods=['GET'])
def index():
    return redirect(url_for('main.get_articles'))


@bp.route("/months", methods=['GET'])
def gets_month():
    item = Wujun.get_max_date()
    if not item:
        return jsonify(data=[], lastUpdate=int(time.time()))
    month = int(item.date[4:6])
    return jsonify(data=range(1, month + 1), lastUpdate=int(time.time()))


@bp.route("/articles", methods=['GET'])
def gets_article():
    month = int(request.args.get("month", 0))
    last_id = int(request.args.get("last_id", 0))

    articles = Wujun.get_new_articles_by_month(month, last_id)
    result = {
        "lastUpdate": int(time.time()),
        "data": map(article_field, articles)
    }
    return jsonify(result)


@bp.route("/article/images", methods=['GET'])
def gets_article_image():
    month = int(request.args.get("month", 1))
    last_id = int(request.args.get("last_id", 0))

    articles = Wujun.get_new_articles_by_month(month, last_id)
    result = {
        "lastUpdate": int(time.time()),
        "data": [_.titleImage for _ in articles],
    }
    return jsonify(result)


@bp.route("/_internal/health")
def health():
    result = dict([(key, str(value)) for key, value in request.headers.items()])
    return jsonify(result)


def article_field(article):
    return {
        "articleId": article.id,
        "title": article.title,
        "titleImage": article.titleImage,
        "commentsCount": article.commentsCount,
        "likesCount": article.likesCount,
        "url": article.url,
        "date": article.date
    }
