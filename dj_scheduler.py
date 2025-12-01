from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from scheduler_email.settings import DEFAULT_FROM_EMAIL
from mailing_list.models import Client, Message, MailingSettings
from mailing_list.management.commands.logger import logger
from django_apscheduler.jobstores import DjangoJobStore

def send_email_to_clients(message_id: int, mailing_id: int) -> None:
    message = Message.objects.get(pk=message_id)
    mailing = MailingSettings.objects.get(pk=mailing_id)
    clients = mailing.client.all()
    list_with_mail = [c.mail for c in clients]

    send_mail(
        subject=message.title_message,
        message=message.body_message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=list_with_mail,
        fail_silently=False
    )
    logger.info('Отправил сообщение!')


scheduler = BackgroundScheduler(timezone='Europe/Moscow')
scheduler.add_jobstore(DjangoJobStore(), 'default')


