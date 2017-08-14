#! coding:utf-8
import time
from flask import request, render_template, url_for, redirect, Blueprint, jsonify

from model import Wujun


bp = Blueprint("main", __name__, url_prefix=None)


@bp.route("/")
def index():
    return redirect(url_for("get_docs"))
    return "work in process"


@bp.route("/articles", methods=['GET'])
def get_articles():
    month = int(request.args.get("month", 1))
    last_id = int(request.args.get("last_id", 0))

    articles = Wujun.get_new_articles_by_month(month, last_id)
    result = {
        "lastUpdate": int(time.time()),
        "articles": map(article_field, articles)
    }
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


@bp.route("/docs", methods=['GET'])
def get_docs():
    return render_template("docs.html")
