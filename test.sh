#!/bin/bash

update_site(){
    cd /data/projects/medtest
    source env/bin/activate
    cd django-shop

    # updating the codebase
    git checkout - . && git fetch && git pull --rebase

    pip install -r requirements.txt
    python manage.py collectstatic --noinput
    python manage.py syncdb
    python manage.py migrate
    python manage.py thumbnail clear

}
export -f update_site

su www-data -c "bash -c update_site"

service uwsgi restart medtest
service nginx force-reload


#python manage.py importyml /data/isells.eu/isells/scripts/medtest.xml --images
