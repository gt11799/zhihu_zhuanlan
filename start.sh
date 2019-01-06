# !/usr/bin/env sh
gunicorn -c gunicorn_config.py wsgi:app
