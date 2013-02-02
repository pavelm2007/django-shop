#!/bin/sh
sudo -i
sudo su www-data -c /bin/bash
cd /data/projects/medtest
source env/bin/activate
cd django-shop

# updating the codebase
git checkout - . && git fetch && git pull --rebase

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py syncdb
python manage.py migrate

exit
service uwsgi restart



#python manage.py importyml /data/isells.eu/isells/scripts/medtest.xml --images
