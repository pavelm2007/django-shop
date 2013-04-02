#!/bin/bash
SOURCE_DIR=$1
SITE_NAME=$2
#update_site(){
    cd /data/projects/${SITE_NAME}
    cp django-shop/local_settings.py local_settings.py.tmp
    rm -fr /data/projects/${SITE_NAME}/django-shop
    cp -r ${SOURCE_DIR} ./django-shop
    mv local_settings.py.tmp django-shop/local_settings.py
sudo chown -R www-data:www-data /data/projects/${SITE_NAME}/django-shop
update_site(){
    source env/bin/activate
    cd django-shop
    pip install -r requirements.txt
    python manage.py collectstatic --noinput
}
export -f update_site

su www-data -c "bash -c update_site"

service uwsgi restart ${SITE_NAME}
service nginx force-reload


#python manage.py importyml /data/isells.eu/isells/scripts/medtest.xml --images

