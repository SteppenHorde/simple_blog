from django.db import models
from django.utils import timezone



class Blog(models.Model):
    pass


class BlogPost(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    text = models.TextField(verbose_name='Текст', help_text='Показывается на страничке поста')
    image = models.ImageField(upload_to='core//images', verbose_name='Картинка', blank=True, null=True)
    pub_date = models.DateTimeField(verbose_name='Дата новости', default=timezone.now)
    published = models.BooleanField(verbose_name='Опубликовать', help_text='Если установлен, то пост будет опубликован', default=False)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Опубликовано недавно?'

    def __str__(self):
        return f'{self.title} (опубликован)' if self.published else self.title
