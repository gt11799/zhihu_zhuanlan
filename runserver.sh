#!/bin/sh

gunicorn -k gevent -w 3 -b 127.0.0.1:4000 wsgi:app
