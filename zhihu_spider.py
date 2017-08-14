#! coding=utf-8
from __future__ import unicode_literals
import uuid
import urlparse
from time import sleep
from datetime import datetime

import requests
from pymongo import MongoClient
from qiniu import Auth, BucketManager
from handle_data import cron_run
from settings import QINIU_AK, QINIU_SK

client = MongoClient('localhost', 27017)
table = client.zhihu.wujun

q = Auth(QINIU_AK, QINIU_SK)
BUCKET_NAME = 'wujunzhuanlan'
bucket = BucketManager(q)

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}

POST_LIST_URL = "https://zhuanlan.zhihu.com/api/columns/wujun/posts?limit=%s&offset=%s"
QINIU_HOST = 'http://7xpxh4.com1.z0.glb.clouddn.com'


def first_get_posts():
    limit = 100
    offset = 0
    while True:
        resp = requests.get(POST_LIST_URL % (limit, offset), headers=HEADER)
        if resp.status_code != 200:
            print resp.data
            print "get wrong"
            break
        posts = resp.json()
        if not posts:
            break
        print "limit: %s, offset: %s, gets: %s" % (limit, offset, len(posts))
        for post in posts:
            save_post(post)
        offset += limit
        sleep(60)


def cron_get_posts():
    limit = 10
    offset = 0
    while True:
        resp = requests.get(POST_LIST_URL % (limit, offset), headers=HEADER)
        if resp.status_code != 200:
            print resp.status_code
            print resp.text
            print "get wrong, http not 200"
            break
        posts = resp.json()
        if not posts:
            break
        print "limit: %s, offset: %s, gets: %s" % (limit, offset, len(posts))
        for post in posts:
            old_post = table.find_one({"slug": post['slug']})
            if old_post:
                print "nothing new"
                raise ValueError("nothing new")
            else:
                print "got a new one"
                save_post(post)
        offset += limit
        sleep(60)
    cron_run()


def save_post(post):
    new_image = upload_image(post['titleImage'])
    post['titleImage'] = new_image
    table.save(post)


def upload_image(url):
    key = str(uuid.uuid1())
    ret, info = bucket.fetch(url, BUCKET_NAME, key)
    return urlparse.urljoin(QINIU_HOST, key)


if __name__ == '__main__':
    print "%s start scripts" % str(datetime.now())
    # cron_get_posts()
    first_get_posts()
    print "%s end scripts" % str(datetime.now())
