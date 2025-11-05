from django.db import models

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
    first_sending_date = models.DateTimeField(verbose_name='дата и время первой отправки рассылки')
    period = models.PositiveSmallIntegerField(verbose_name='периодичность')
    mailing_status = models.BooleanField(default=False, verbose_name='статус')
    message = models.ForeignKey(Message, default=None, on_delete=models.CASCADE, to_field='id',
                                verbose_name='сообщение')
    client = models.ForeignKey(Client, default=None, to_field='id', on_delete=models.CASCADE, verbose_name='клиент')
    # day='*/10' → каждые 10 дней

    def __str__(self):
        return f'{self.first_sending_date, self.period, self.mailing_status}'

    class Meta:
        verbose_name = 'настройка рассылки'
        verbose_name_plural = 'настройки рассылки'


class MailingAttempt(models.Model):
    last_attempt_date = models.DateTimeField(verbose_name='дата и время последней попытки')
    attempt_status = models.BooleanField(default=False, verbose_name='статус попытки')
    mail_service_response = models.TextField(default=None, verbose_name='ответ почтового сервиса')

    def __str__(self):
        return f'{self.attempt_status}, {self.last_attempt_date}, {self.mail_service_response}'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
