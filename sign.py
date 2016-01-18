# coding: utf-8
import hashlib
import time

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


def gen_sign(timestamp):
    md = hashlib.sha1(str(timestamp) + TOKEN)
    first_level = md.hexdigest()
    md = hashlib.sha1(first_level + TOKEN)
    sign_gen = md.hexdigest()
    return sign_gen[:10]
