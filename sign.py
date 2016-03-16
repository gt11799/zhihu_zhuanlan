# coding: utf-8
import time
import hmac
import hashlib

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


def gen_sign(date, body):
    obj = hmac.new(TOKEN, date + body, hashlib.sha1)
    return obj.hexdigest()
