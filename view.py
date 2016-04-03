#! coding:utf-8
import json
from flask import Flask, request, render_template, url_for, redirect

from model import Wujun
from sign import gen_sign
from settings import DEBUG, TOKEN


app = Flask(__name__)
app.debug = DEBUG


@app.route("/")
def index():
    return redirect(url_for("get_docs"))
    return "work in process"


@app.route("/articles", methods=['GET'])
def get_articles():
    month = int(request.args.get("month", 1))
    last_id = int(request.args.get("last_id", 0))

    articles = Wujun.get_new_articles_by_month(month, last_id)
    return json.dumps(map(article_field, articles))


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
    values = request.values
    authorization = request.headers.get('Authorization')
    sign = gen_sign(date, body)
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
