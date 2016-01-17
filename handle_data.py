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
REGEX = re.compile(u"\d{1,2}月\d{1,2}日")
REGEX_MONTH = re.compile(u"\d{1,2}月")
REGEX_DAY = re.compile(u"\d{1,2}日")

ZHUANLAN_HOST = "http://zhuanlan.zhihu.com"


def handle_data(skip, limit):
    data = table.find({
        "title": {"$regex": REGEX_TITLE}
    },
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
        return None
    pattern = pattern.group()
    month = REGEX_MONTH.search(pattern)
    if not month:
        return None
    month = month.group().replace(u"月", "")
    day = REGEX_DAY.search(pattern)
    if not day:
        return None
    day = day.group().replace(u"日", "")
    dt = datetime(year=2015, month=int(month), day=int(day))
    return dt.strftime("%Y%m%d")

if __name__ == '__main__':
    handle_data(0, 1)
