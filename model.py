# coding: utf-8

import peewee

from settings import DB_USER, DB_PASSWD

database = peewee.MySQLDatabase("zhuanlan", host="localhost", user=DB_USER,
                                passwd=DB_PASSWD)


class Model(peewee.Model):

    class Meta:
        database = database


class Wujun(Model):

    code = peewee.CharField()
    title = peewee.CharField()
    titleImage = peewee.CharField()
    date = peewee.CharField()
    likesCount = peewee.CharField()
    commentsCount = peewee.CharField()
    url = peewee.CharField()
    created = peewee.CharField()
    updated = peewee.CharField()

database.connect()
