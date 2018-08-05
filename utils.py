#! coding:utf-8
import json
from flask import Response


def fail(http_code, message):
    data = dict(message=message)
    return Response(json.dumps(data), status=http_code, mimetype='application/json')


def success(data):
    # 以后应该加上code，再使用这个
    return
