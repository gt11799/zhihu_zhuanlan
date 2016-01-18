#! coding:utf-8
import json
from flask import Flask, request

from model import Wujun
from sign import check_sign

app = Flask(__name__)


@app.route("/")
def index():
    return "work in process"


@app.route("/articles", methods=['GET'])
def get_articles():
    page = int(request.args.get("page", 0))
    per_page = int(request.args.get("per_page", 30))
    last_id = int(request.args.get("last_id", 0))

    articles = Wujun.get_new_articles(last_id, page, per_page)
    return json.dumps(map(article_field, articles))


def article_field(article):
    return {
        "id": article.id,
        "title": article.title,
        "titleImage": article.titleImage,
        "commentsCount": article.commentsCount,
        "likesCount": article.likesCount,
        "url": article.url,
        "date": article.date
    }


@app.route("/test_sign", methods=['GET'])
def test_sign():
    timestamp = request.args.get("t")
    sign = request.args.get("s")
    passed, error = check_sign(timestamp, sign)
    if passed:
        return "success!"
    else:
        return error


@app.route("/docs", methods=['GET'])
def get_docs():
    return


if __name__ == "__main__":
    app.run(debug=True)
