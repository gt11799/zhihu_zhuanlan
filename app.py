#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import traceback
from flask import Flask, request, current_app, g, render_template

from settings import DEBUG, LOG_PATH
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
        'file': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'formatter': 'file_format',
            'filename': '/tmp/zhihu.log',
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
            'handlers': ['file'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    },
}


def create_app(name=None, _config=None):
    app = Flask(name or __name__)
    app.debug = DEBUG

    init_logging(app)
    init_request_log(app)

    app.register_blueprint(main_bp)

    return app


def load_configs(app):
    for name, value in config.iteritems():
        app.config[name] = value


def init_logging(app):
    if not app.debug and not app.config['TESTING']:
        import logging
        import logging.config
        LOGGING_CONFIG['handlers']['file']['filename'] = LOG_PATH
        logging.config.dictConfig(LOGGING_CONFIG)
    else:
        import logging
        logging.basicConfig(level='DEBUG')


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
