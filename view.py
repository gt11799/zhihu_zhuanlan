#! coding:utf-8
import time
from flask import request, url_for, redirect, Blueprint, jsonify

from sign import check_sign
from model import Wujun


bp = Blueprint("main", __name__, url_prefix=None)


@bp.route("/", methods=['GET'])
def index():
    return redirect(url_for('main.gets_article'))


@bp.route("/months", methods=['GET'])
@check_sign
def gets_month():
    item = Wujun.get_max_date()
    if not item:
        return jsonify(data=[], lastUpdate=int(time.time()))
    month = int(item.date[4:6])
    return jsonify(data=range(1, month + 1), lastUpdate=int(time.time()))


@bp.route("/articles", methods=['GET'])
# @check_sign
def gets_article():
    month = int(request.args.get("month", 0))
    last_update = int(request.args.get("last_update", 0))

    articles = Wujun.get_new_articles_by_month(month, last_update)
    result = {
        "lastUpdate": int(time.time()),
        "data": map(article_field, articles)
    }
    return jsonify(result)


@bp.route("/article/images", methods=['GET'])
@check_sign
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


@bp.route("/_internal/sign_test")
def test_sign():
    from sign import *
    import json
    ts = request.headers.get('X-TS')
    qs = request.args.to_dict()
    data = copy(qs)
    data['ts'] = ts
    string = sort_query_string(data)
    token = 'Bearer %s' % generate_token(string)
    token_given = request.headers.get('Authorization')
    data = dict(ts=ts, qs=qs, to_sign_data=data, to_sign_string=string, token=token, token_given=token_given)
    return jsonify(data=data)


def article_field(article):
    return {
        "articleId": article.id,
        "title": article.title,
        "titleImage": article.titleImage,
        "commentsCount": article.commentsCount,
        "likesCount": article.likesCount,
        "url": article.url,
        "date": article.date,
        "updated": datetime_to_timestamp(article.updated),
    }


def datetime_to_timestamp(dt):
    t = dt.timetuple()
    return time.mktime(t)
