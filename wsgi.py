#! coding: utf-8
from werkzeug.contrib.fixers import ProxyFix

from app import create_app


app = create_app('zhuanlan')
app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5005)
