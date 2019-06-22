from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models.blog import Blog



@receiver(post_save, sender=User)
def create_blog(sender, instance, created, **kwargs):
    if created:
        author_username = instance.username
        title = f"{author_username}' blog" if author_username[-1] == 's' else f"{author_username}'s blog"
        Blog.objects.create(author=instance, title=title)
