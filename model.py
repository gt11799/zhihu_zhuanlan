# coding: utf-8

import peewee


database = peewee.SqliteDatabase("zhuanlan.db")


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

    @classmethod
    def get_articles(cls, last_id, page=0, per_page=30):
        return cls.select().where(
            cls.id > last_id).paginate(page, per_page)

    @classmethod
    def get_new_articles_by_month(cls, month, last_id):
        return cls.select().where(
            cls.id > last_id,
            cls.date.startswith("2015%02d" % month))


database.connect()
