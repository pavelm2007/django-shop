from optparse import make_option
from django.conf import settings
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--delete',
                    action='store_true',
                    dest='delete',
                    default=True,
                    help='Delete poll instead of closing it'),
    ) + (
                      make_option('--images',
                                  action='store_true',
                                  dest='images',
                                  default=False,
                                  help='Import images from YML'),
                  )
    help = 'Generates local_setting.py based on ORM Settings'

    def handle(self, *args, **options):
        # opens file for writing
        print settings.PROJECT_DIR + 'local_settings.py'
        local_setting = open(os.path.join(settings.PROJECT_DIR, 'local_settings.py'), "w")

        local_setting.write("""
TIME_ZONE = 'Europe/Kiev'

LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('ru', 'Russian'),
    )

DEFAULT_LANGUAGE = 1

CURRENCY = 'UAH'
        """)
        local_setting.close()
