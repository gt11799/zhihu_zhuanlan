#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.config
from flask import Flask, request, current_app

from view import bp as main_bp


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'console_format': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'file_format': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console_format',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'console': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'file': {
            'level': 'WARNING',
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
}


def create_app(name=None, _config=None):
    app = Flask(name or __name__)

    init_logging(app)
    init_request_log(app)

    app.register_blueprint(main_bp)

    return app


def init_logging(app):
    logging.config.dictConfig(LOGGING_CONFIG)


def _request_log(resp, *args, **kws):
    current_app.logger.info(
        '%s request: [%s] %s, url: %s, '
        'args: %s, form: %s, json: %s',
        request.remote_addr,
        resp.status, request.method, request.url,
        request.args,
        request.form,
        request.get_json(silent=True))
    return resp


def init_request_log(app):
    app.after_request(_request_log)
