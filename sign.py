# coding: utf-8
import time
import hmac
import hashlib
import base64

from settings import TOKEN, TIMEOUT
from log import logger


def check_sign(timestamp, sign):
    if not timestamp or not sign:
        return False, "arguments lost"
    delta = int(time.time()) - int(timestamp)
    logger.info(delta)
    if delta < -1 or delta > TIMEOUT:
        return False, "timeout"
    sign_gen = gen_sign(timestamp)
    if sign_gen == sign:
        return True, ""
    return False, "sign error"


def gen_sign(body):
    obj = hmac.new(TOKEN, body, hashlib.sha1)
    return obj.hexdigest()


def get_sort_string(data, date):
    data = sorted(data.items(), cmp=lambda x, y: cmp(x[0], y[0]))
    string = "".join(["%s=%s" % (_[0], _[1]) for _ in data])
    string_hash = base64.b64encode(get_hash(string))
    return string_hash + '\n' + date


def get_hash(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()
