from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models



class MyUserManager(UserManager):
    def create_user():
        user = User()
        blog = Blog(author=user)
        return user


class User(AbstractUser):
    objects = MyUserManager()
    def __str__(self):
        return self.email


class Blog(models.Model):
    author = OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class BlogPost(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    text = models.TextField(verbose_name='Текст', help_text='Показывается на страничке поста')
    image = models.ImageField(upload_to='core/blog/images', verbose_name='Картинка', blank=True, null=True)
    pub_date = models.DateTimeField(verbose_name='Дата', default=timezone.now)
    published = models.BooleanField(verbose_name='Опубликовать', help_text='Если установлен, то пост будет опубликован', default=False)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Опубликовано недавно?'

    def __str__(self):
        return f'{self.title} (опубликован)' if self.published else self.title
