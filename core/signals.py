from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models.blog import Blog



@receiver(post_save, sender=User)
def create_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(author=instance)
