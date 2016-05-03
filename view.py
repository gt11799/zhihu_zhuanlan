#! coding:utf-8
import time
import json
import base64
import hashlib
from flask import Flask, request, render_template, url_for, redirect, Blueprint

from model import Wujun
from sign import check_sign
from settings import DEBUG, TOKEN


app = Flask(__name__)
app.debug = DEBUG

bp = Blueprint("main", __name__, url_prefix=None)


@app.route("/")
def index():
    return redirect(url_for("get_docs"))
    return "work in process"


@app.route("/articles", methods=['GET'])
@check_sign
def get_articles():
    month = int(request.args.get("month", 1))
    last_id = int(request.args.get("last_id", 0))

    articles = Wujun.get_new_articles_by_month(month, last_id)
    result = {
        "lastUpdate": int(time.time()),
        "articles": map(article_field, articles)
    }
    return json.dumps(result)


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


@app.route("/test_sign", methods=['GET', 'POST'])
def test_sign():
    date = request.headers.get('Date') or ""
    body = request.data or ""
    params = request.args
    data = sorted(params.items(), cmp=lambda x, y: cmp(x[0], y[0]))
    string = "".join(["%s=%s" % (_[0], _[1]) for _ in data])
    string_hash = base64.b64encode(get_hash(string))
    string_done = string_hash + '\n' + date
    authorization = request.headers.get('Authorization')
    sign = gen_sign(string)
    if authorization == sign:
        result = "success"
    else:
        result = "fail"
    return render_template("test_sign.html", token=TOKEN, **locals())


@app.route("/docs", methods=['GET'])
def get_docs():
    return render_template("docs.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
