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
    likesCount = peewee.IntegerField()
    commentsCount = peewee.IntegerField()
    url = peewee.CharField()
    created = peewee.DateTimeField()
    updated = peewee.DateTimeField()

    @classmethod
    def get_max_code(cls):
        wujun = cls.select(cls.code).order_by(
            cls.code.desc()
        ).limit(1)
        if not wujun:
            return 0
        return wujun.get().code


database.connect()
