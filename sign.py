# coding: utf-8
import time
import hmac
import hashlib
import base64
from functools import wraps
from flask import Response, request

from log import logger
from settings import TOKEN, TIMEOUT


def check_sign(view_func):
    @wraps(view_func)
    def _(*args, **kwargs):
        date = request.headers.get('Date') or ""
        authorization = request.headers.get('Authorization')
        if authorization is None:
            return Response(status=401)
        params = request.args.to_dict()
        forms = request.form.to_dict()
        params.update(forms)
        string = get_sort_string(params, date)
        sign = gen_sign(string)

        if authorization != sign:
            return Response(status=403)
        return view_func(*args, **kwargs)
    return _


def gen_sign(body):
    obj = hmac.new(TOKEN, body, hashlib.sha1)
    return base64.b64encode(obj.hexdigest())


def get_sort_string(data, date):
    data = sorted(data.items(), cmp=lambda x, y: cmp(x[0], y[0]))
    string = "".join(["%s=%s" % (_[0], _[1]) for _ in data])
    string_hash = base64.b64encode(get_hash(string))
    return string_hash + '\n' + date


def get_hash(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()
