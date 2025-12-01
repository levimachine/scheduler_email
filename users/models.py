from django.contrib.auth.models import AbstractUser
from django.db import models
from mailing_list.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    first_name = models.CharField(max_length=50, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', **NULLABLE)
    phone = models.CharField(max_length=30, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='media/users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=70, verbose_name='Страна', **NULLABLE)
    secret_key = models.CharField(max_length=15, **NULLABLE)
    is_verify = models.BooleanField(default=False, verbose_name='Верификация', **NULLABLE)
    user_input_secret_key = models.CharField(max_length=15, verbose_name='Секретный ключ', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


