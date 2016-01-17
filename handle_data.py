# coding: utf-8
import re
import MySQLdb
import urlparse
from pymongo import MongoClient

from settings import DB_USER, DB_PASSWD

client = MongoClient('localhost', 27017)
table = client.zhihu.wujun

mysqldb = MySQLdb.Connect("localhost", user=DB_USER, passwd=DB_PASSWD,
                          db="zhuanlan")


def handle_data(skip, limit):
    data = table.find({}, {
        "_id": -1,
        "slug": 1,
        "titleImage": 1,
        "likesCount": 1,
        "commentsCount": 1,
        "title": 1,
        "url": 1,
    }).sort([("slug", 1)]).skip(skip).limit(limit)
    for item in data:
        pass


if __name__ == '__main__':
    first_handle()
