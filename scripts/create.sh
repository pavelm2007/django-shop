#!/bin/bash

if test -z "$1"
then
    echo "Error: site name is not set!"
    exit 0
else
    SOURCE_DIR=$1
fi

if test -z "$2"
then
    echo "Error: site name is not set!"
    exit 0
else
    SITE_NAME=$2
fi

if test -z "$2"
then
    echo "Error: site domain is not set!"
    exit 0
else
    SITE_DOMAIN=$3
fi

# That will remove the directory if it's present, otherwise do nothing.
rm -rf /data/projects/${SITE_NAME}

mkdir /data/projects/${SITE_NAME}
cd /data/projects/${SITE_NAME}
cp -r ${SOURCE_DIR} ./django-shop
mkdir static
mkdir media
mkdir logs
sudo chown -R www-data:www-data /data/projects/${SITE_NAME}

init_site(){
    cd /data/projects/${SITE_NAME};
    virtualenv --system-site-packages env;
    source env/bin/activate;
    cd django-shop
    pip install -r requirements.txt
    python manage.py collectstatic --noinput

echo "
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '${SITE_NAME}',
        'USER': 'root',
        'PASSWORD': 'baster551737',
        'HOST': 'isells.cbiec5vjmqef.us-east-1.rds.amazonaws.com',
        'PORT': '',
    }
}
DEBUG = False
" > local_settings.py

    # creating a database
    mysql -h isells.cbiec5vjmqef.us-east-1.rds.amazonaws.com -uroot -pbaster551737 -e "DROP DATABASE IF EXISTS ${SITE_NAME}; CREATE DATABASE ${SITE_NAME} CHARACTER SET='utf8';"
    python manage.py syncdb --migrate --noinput
    python manage.py createcachetable my_cache_table
    #python manage.py createsuperuser --username=admin --email=a@dmin.com

    # adding a Django super-user
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@${SITE_DOMAIN}', 'admin')" | python manage.py shell

    # importing a demo products
    python manage.py importyml /data/isells/isells/scripts/demo_site_data_yml.xml --images
}

export SITE_NAME=${SITE_NAME}
export -f init_site

su www-data -c "bash -c init_site"

# adding nginx config
echo "
server {
    listen  80;
    server_name ${SITE_DOMAIN};
    access_log /data/projects/${SITE_NAME}/logs/nginx_access.log;
    error_log /data/projects/${SITE_NAME}/logs/nginx_error.log;

    location / {
        uwsgi_pass  unix:///var/run/uwsgi/app/${SITE_NAME}/socket;
        include     uwsgi_params;
    }

    location /media/  {
        alias /data/projects/${SITE_NAME}/media/;
    }

    location  /static/ {
        alias /data/projects/${SITE_NAME}/static/;
    }
}
" > /etc/nginx/sites-enabled/${SITE_NAME}

# adding uwsgi config
echo "
[uwsgi]
vhost = true
plugins = python
master = true
enable-threads = true
processes = 1
wsgi-file = /data/projects/${SITE_NAME}/django-shop/core/wsgi.py
virtualenv = /data/projects/${SITE_NAME}/env
chdir = /data/projects/${SITE_NAME}/django-shop/
touch-reload = /data/projects/${SITE_NAME}/django-shop/reload
" > /etc/uwsgi/apps-enabled/${SITE_NAME}.ini

service uwsgi restart ${SITE_NAME}
service nginx restart

exit 0