from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from slugify import slugify

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    mail = models.EmailField(max_length=100, verbose_name='почта')
    fullname = models.CharField(max_length=200, verbose_name='полное имя')
    comment = models.TextField(verbose_name='комментарий')

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    title_message = models.CharField(max_length=200, verbose_name='тема письма')
    body_message = models.TextField(verbose_name='тело письма')

    def __str__(self):
        return self.title_message

    class Meta:
        verbose_name = 'сообщение для рассылки'
        verbose_name_plural = 'сообщения для рассылки'


class MailingSettings(models.Model):
    title = models.CharField(max_length=200, default='', verbose_name='Название рассылки')
    first_sending_date = models.DateTimeField(verbose_name='дата и время первой отправки рассылки')
    period = models.PositiveSmallIntegerField(verbose_name='периодичность')
    mailing_status = models.CharField(default=False, choices=[
        ('created', 'Создана'),
        ('running', 'Активна'),
        ('completed', 'Завершена')], verbose_name='статус')
    message = models.ForeignKey(Message, default=None, on_delete=models.CASCADE, to_field='id',
                                verbose_name='сообщение')
    client = models.ManyToManyField(Client, default=None, related_name='mailing', verbose_name='клиент')

    # day='*/10' → каждые 10 дней

    def __str__(self):
        return f'{self.first_sending_date, self.period, self.mailing_status}'

    class Meta:
        verbose_name = 'настройка рассылки'
        verbose_name_plural = 'настройки рассылки'


class MailingAttempt(models.Model):
    mailing = models.OneToOneField(MailingSettings, default=False, on_delete=models.CASCADE, related_name='log',
                                   verbose_name='рассылка')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='URL slug')
    last_attempt_date = models.DateTimeField(**NULLABLE, verbose_name='дата и время последней попытки')
    attempt_status = models.BooleanField(**NULLABLE, default=False, verbose_name='статус попытки')
    mail_service_response = models.TextField(**NULLABLE, default=None, verbose_name='ответ почтового сервиса')

    def __str__(self):
        return f'{self.attempt_status}, {self.last_attempt_date}, {self.mail_service_response}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.mailing.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'


@receiver(post_save, sender=MailingSettings)
def create_mailing_log(sender, instance, created, **kwargs):
    if created:
        MailingAttempt.objects.create(mailing=instance)


