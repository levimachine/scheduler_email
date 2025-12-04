from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание статьи')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров', blank=True, null=True)
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
