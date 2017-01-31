#!/bin/bash

DEPLOY_DIR=/home/www/python
CURRENT_DIR=$DEPLOY_DIR/current
NAME="celery"                                     # Name of the application
DJANGODIR=$CURRENT_DIR         		              # Django project directory
USER=www
DJANGO_SETTINGS_MODULE=root.settings.prod.vps     # which settings file should Django use
DJANGO_WSGI_MODULE=root.wsgi                      # WSGI module name

echo "Starting $NAME"

# Activate the virtual environment
export HOME=/home/$USER
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon env

cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec celery -A root worker -l info
