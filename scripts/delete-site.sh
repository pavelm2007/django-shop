#!/bin/bash
if test -z "$1"
then
    echo "Error: site name is not set!"
    exit 0
else
    SITE_NAME=$1
fi

# NGINX block the site from www-access
rm /etc/nginx/sites-enabled/${SITE_NAME}
service nginx reload

# uWSGI stop
uwsgi --stop /var/run/uwsgi/app/${SITE_NAME}/pid

# - configs
rm    /etc/uwsgi/apps-enabled/${SITE_NAME}.ini
rm -r /var/run/uwsgi/app/${SITE_NAME}/

# FILES
rm -r /data/projects/${SITE_NAME}/

# MySQL drop DB
#mysql -h isells.cbiec5vjmqef.us-east-1.rds.amazonaws.com -uroot -pbaster551737 -e "DROP DATABASE IF EXISTS ${SITE_NAME}"
mysql -h 85.119.157.185 -uisells -pvdlk39dG46isells -e "DROP DATABASE IF EXISTS ${SITE_NAME}"

exit 0