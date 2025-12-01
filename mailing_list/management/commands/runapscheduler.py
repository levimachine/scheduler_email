from mailing_list.management.commands.logger import logger
from django.conf import settings

from mailing_list.models import Client
from scheduler_email.settings import DEFAULT_FROM_EMAIL
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.core.mail import send_mail




def send_email_to_clients():
    client_list = []
    for mail in Client.objects.all():
        client_list.append(mail.mail)

    send_mail(
        subject='Рассылка от Женька',
        message='Поздравляю, рассылка удалась!',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=client_list,
        fail_silently=False
    )
    logger.info('Отправил сообщение!')


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        scheduler.add_job(
            send_email_to_clients,
            trigger=CronTrigger(second='*/10'),
            id='send_email_to_clients',
            max_instances=1,
            replace_existing=True
        )
        logger.info('Added job "send_email_to_clients" ')

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week='mon', hour='00', minute='00'),
            id='delete_old_job_executions',
            max_instances=1,
            replace_existing=True
        )

        logger.info('Added weekly job: "delete_old_job_executions"')

        try:
            logger.info('Scheduler started...')
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            logger.info('Scheduler shut down successfully!')
