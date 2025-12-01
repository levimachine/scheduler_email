from time import sleep
from django.apps import AppConfig
from mailing_list.management.commands.logger import logger
import os


class MailingListConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing_list'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return

        sleep(1.5)
        from dj_scheduler import scheduler

        try:
            scheduler.start()
            logger.info('Шедулер запустился!')

        except KeyboardInterrupt:
            scheduler.shutdown()
            logger.info('Шедулер закончил работу!')
