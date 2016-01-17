# coding: utf-8
import re
import MySQLdb
import urlparse
from datetime import datetime
from pymongo import MongoClient

from settings import DB_USER, DB_PASSWD
from log import logger
from model import Wujun


client = MongoClient('localhost', 27017)
table = client.zhihu.wujun

mysqldb = MySQLdb.Connect("localhost", user=DB_USER, passwd=DB_PASSWD,
                          db="zhuanlan")

REGEX_TITLE = u".*发明365.*"
REGEX = re.compile(u"\d{1,2}月\d{1,2}")

ZHUANLAN_HOST = "http://zhuanlan.zhihu.com"


def handle_data(query, skip, limit):
    data = table.find(query,
                      {
                          "_id": 0,
                          "slug": 1,
                          "titleImage": 1,
                          "likesCount": 1,
                          "commentsCount": 1,
                          "title": 1,
                          "url": 1,
                      }).sort([("slug", 1)]).skip(skip).limit(limit)
    articles = []
    for item in data:
        logger.info("will handle article: %s" % item['slug'])
        date = get_date(item['title'])
        if not date:
            logger.error("get date wrong")
            logger.error(item['title'])
            continue
        item['code'] = item.pop("slug")
        item['date'] = date
        item['url'] = urlparse.urljoin(ZHUANLAN_HOST, item['url'])
        articles.append(item)
    if articles:
        Wujun.insert_many(articles).execute()
    else:
        logger.info("no data insert")


def get_date(title):
    # get date from title
    # return 20150809
    pattern = REGEX.search(title)
    if not pattern:
        logger.info("not found date")
        return None
    pattern = pattern.group()
    month, day = pattern.split(u"月")
    dt = datetime(year=2015, month=int(month), day=int(day))
    return dt.strftime("%Y%m%d")


def first_run():
    query = {
        "title": {"$regex": REGEX_TITLE}
    }
    count = table.find(query).count()
    per = 50
    for start in range(count + per)[::per]:
        logger.info("run start: %s" % start)
        handle_data(start, per)


def cron_run():
    max_code = Wujun.get_max_code()
    query = {
        "title": {"$regex": REGEX_TITLE},
        "slug": {"$gt": int(max_code)}
    }
    count = table.find(query).count()
    handle_data(query, 0, count)


if __name__ == '__main__':
    cron_run()
