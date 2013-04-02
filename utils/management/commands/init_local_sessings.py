import os

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Setting


class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = 'Generates local_setting.py based on ORM Settings'

    def handle(self, *args, **options):

        try:
            orm_settings = Setting.objects.filter(is_active=True)[0]
        except Setting.DoesNotExist:
            print "Setting.DoesNotExist"
            return False

        # opens file for writing
        local_setting = open(os.path.join(settings.PROJECT_DIR, 'local_settings.py'), "w")

        # timezone
        local_setting.write("TIME_ZONE = '%s'" % 'Europe/Kiev' + '\n')

        # language
        local_setting.write("DEFAULT_LANGUAGE = 1" + '\n')
        local_setting.write("LANGUAGE_CODE = '%s'" % 'ru' + '\n')
        local_setting.write("LANGUAGES = (('%s', '%s'),)" % ('ru', 'Russian') + '\n')

        # currency
        local_setting.write("CURRENCY = '%s'" % orm_settings.currency + '\n')

        # database
        # todo: rewrite this hack
        site_database = os.path.basename(os.path.realpath(os.path.join(settings.PROJECT_DIR, '..')))

        local_setting.write(
            "DATABASES = {'default': { 'ENGINE': 'django.db.backends.mysql', 'NAME': '%s', 'USER': 'isells',"
            "'PASSWORD': 'vdlk39dG46isells', 'HOST': '85.119.157.185' }}" % site_database + '\n')

        # debug
        local_setting.write("DEBUG = False" + '\n')

        local_setting.close()
