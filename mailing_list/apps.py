from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from mailing_list.management.commands.logger import get_logger


class MailingListConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing_list'

    def ready(self):
        from django_apscheduler.jobstores import DjangoJobStore

        logger = get_logger('scheduler.log')
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        try:
            scheduler.start()
            logger.info('Шедулер запустился!')

        except KeyboardInterrupt:
            scheduler.shutdown()
            logger.info('Шедулер закончил работу!')
