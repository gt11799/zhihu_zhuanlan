#! coding: utf-8
from werkzeug.contrib.fixers import ProxyFix

from view import app


app.wsgi_app = ProxyFix(app.wsgi_app)
