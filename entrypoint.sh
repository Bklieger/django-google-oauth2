#!/bin/sh

gunicorn --bind 0.0.0.0:8000 --workers 4 -k uvicorn.workers.UvicornWorker djgoprod.wsgi:application