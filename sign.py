#! coding:utf-8
import hmac
import time
import hashlib
from copy import copy
from functools import wraps
from flask import request

from utils import fail


def sort_query_string(data):
    sorted_data = sorted(data.items(), key=lambda x: x[0])
    values = ['%s=%s' % _ for _ in sorted_data]
    return '&'.join(values)


def generate_token(string):
    from settings import SECRET_KEY
    return hmac.new(SECRET_KEY, str(string), hashlib.sha1).hexdigest()


def check_sign(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        qs = request.args.to_dict()
        ts = request.headers.get('X-TS')
        token = request.headers.get('Authorization')
        if not token:
            return fail(403, 'token not found')
        token = token.split(' ')
        if len(token) < 2 or token[0] != 'Bearer':
            return fail(403, 'token type error')
        if (not ts) or abs(int(time.time()) - int(ts)) > 2000:
            return fail(403, 'sign expired')

        data = copy(qs)
        data['ts'] = ts
        string = sort_query_string(data)
        token_gen = generate_token(string)
        if token_gen != token[1]:
            return fail(403, 'token error')
        return func(*args, **kwargs)
    return wrapper
