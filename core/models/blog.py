from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User



class Blog(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subscribers = models.ManyToManyField(User, related_name='subscribers_blog_set', blank=True)
    title = models.CharField(verbose_name='Название блога (по дефолту берётся от имени автора, но можно сменить вручную)', max_length=100)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    read = models.ManyToManyField(User, related_name='read_blogpost_set', blank=True)
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    text = models.TextField(verbose_name='Текст', help_text='Показывается на страничке поста')
    image = models.ImageField(upload_to='core/blog/images', verbose_name='Картинка', blank=True, null=True)
    pub_date = models.DateTimeField(verbose_name='Дата создания/публикации', default=timezone.now)
    published = models.BooleanField(verbose_name='Опубликовать', help_text='Если установлен, то пост будет опубликован', default=False)

    def __str__(self):
        return f'{self.title} (опубликован)' if self.published else self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Опубликовано недавно?'

    def get_absolute_url(self):
        # поле author является pk для Blog, поэтому id у них совпадают:
        blog_id = self.blog.author.id # == user_id
        return reverse('show_post', kwargs={
                                            'blog_id': blog_id,
                                            'post_id': self.pk,
                                            })
