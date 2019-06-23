from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail

from django.contrib.auth.models import User
from .models.blog import Blog, BlogPost



@receiver(post_save, sender=User)
def create_blog(sender, instance, created, **kwargs):
    if created:
        author_username = instance.username
        title = f"{author_username}' blog" if author_username[-1] == 's' else f"{author_username}'s blog"
        Blog.objects.create(author=instance, title=title)


@receiver(post_save, sender=BlogPost)
def send_email_note_of_a_new_post(sender, instance, created, **kwargs):
    if created:
        post = instance
        post_url = post.get_absolute_url()
        blog = post.blog
        author_username = blog.author.username
        blog_title = blog.title
        # вытаскиваем только тех подписчиков, которые имеют почту:
        subscribers_with_emails = blog.subscribers.all().exclude(email__isnull=True).exclude(email__exact='')
        recipient_list = [subscriber.email for subscriber in subscribers_with_emails]

        subject = f'Новый пост в блоге {blog_title} автора {author_username}'
        message = f'В блоге {blog_title} появился новый пост!\nСсылка: {post_url}'
        from_email = 'simpleblog@example.com'
        datatuple = tuple((subject, message, from_email, [to_email]) for to_email in recipient_list)
        print(datatuple)
        send_mass_mail(
                    datatuple,
                    fail_silently=False,
        )
