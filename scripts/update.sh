#!/bin/bash
if test -z "$1"
then
    echo "source directory is not set!"
    exit 0
else
    SOURCE_DIR=$1
fi

if test -z "$2"
then 
    echo "site name is not set!" 
    exit 0
else
    SITE_NAME=$2
fi
HOME_PATH=/data/projects
cd ${HOME_PATH}/${SITE_NAME}
cp django-shop/local_settings.py local_settings.py.tmp
rm -fr ${HOME_PATH}/${SITE_NAME}/django-shop
cp -r ${SOURCE_DIR} ./django-shop
mv local_settings.py.tmp django-shop/local_settings.py
sudo chown -R www-data:www-data ${HOME_PATH}/${SITE_NAME}/django-shop
update_site(){
    cd ${HOME_PATH}/${SITE_NAME}
    source env/bin/activate
    cd django-shop
    pip install -r requirements.txt
    python manage.py collectstatic --noinput
}
export -f update_site

su www-data -c "bash -c update_site"

service uwsgi restart ${SITE_NAME}
#service nginx force-reload
