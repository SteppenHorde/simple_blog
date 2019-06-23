from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import generic, View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models.blog import Blog, BlogPost



class Main(TemplateView): # персональная лента новостей
    template_name = 'core/main.html'
    def get_context_data(self, *args, **kwargs):
        is_authenticated = self.request.user.is_authenticated
        if is_authenticated: # если user авторизован
            user_id = self.request.user.id
            user = User.objects.get(id=user_id)
            # вытаскиваем все посты из всех блогов, на которые user подписан
            posts_list = BlogPost.objects.filter(
                                                blog__subscribers=user
                                                ).order_by('-pub_date')
            # собираем все прочитанные посты:
            read_posts = set()
            for post in posts_list:
                post_read = post.read # список тех, кто отметил пост прочитанным
                if post.read.all().filter(id=user_id).exists(): # .get(id=user_id) => exception
                    read_posts.add(post)

            context = {
                'posts_list': posts_list,
                'read_posts': read_posts,
            }
        else:
            context = {}

        return context


class Blogs(TemplateView): # список всех блогов
    template_name = 'core/blogs.html'

    def get_context_data(self, *args, **kwargs):
        all_blogs_query_set = Blog.objects.all()
        all_blogs_set = set()

        if self.request.user.is_authenticated:
            is_authenticated = True
            user_id = self.request.user.id
            user = User.objects.get(id=user_id)
        else:
            is_authenticated = False
        # проверяем для каждого блога, является ли данный пользователь подписчиком:
        for blog in all_blogs_query_set:
            blog_subscribers = blog.subscribers
            if is_authenticated:
                is_subscriber = blog_subscribers.all().filter(id=user_id).exists()
            else:
                is_subscriber = False
            all_blogs_set.add((blog, is_subscriber))

        context = {
            'blogs_set': all_blogs_set,
        }

        #return render(request, self.template_name, context=context)
        return context


class ShowBlog(TemplateView): # отдельный блог со всеми постами
    template_name = 'core/show_blog.html'

    def get_context_data(self, *args, **kwargs):
        blog_id = kwargs['blog_id']
        # поле author является pk для Blog, поэтому id у них совпадают:
        blog = Blog.objects.get(author_id=blog_id)
        posts_list = blog.blogpost_set.all().order_by('-pub_date')

        read_posts = set()
        # проверяем, является ли данный пользователь подписчиком:
        # поле author является pk для Blog, поэтому id у них совпадают:
        is_authenticated = self.request.user.is_authenticated
        if is_authenticated:
            user_id = self.request.user.id
            blog_subscribers = blog.subscribers
            # вытаскиваем всех подписчиков и смотрим, есть ли среди них user
            is_subscriber = blog_subscribers.all().filter(id=user_id).exists()
            # заодно собираем все прочитанные посты:
            for post in posts_list:
                if post.read.all().filter(id=user_id).exists(): # .get(id=user_id) => исключение
                    read_posts.add(post)
        else:
            is_subscriber = False
        context = {
            'blog': blog,
            'posts_list': posts_list,
            'is_subscriber': is_subscriber,
            'read_posts': read_posts,
        }

        return context


class ShowPost(TemplateView): # отдельный пост
    template_name = 'core/show_post.html'

    def get_context_data(self, *args, **kwargs):
        blog_id = kwargs['blog_id']
        post_id = kwargs['post_id']
        # поле author является pk для Blog, поэтому id у них совпадают:
        blog = Blog.objects.get(author_id=blog_id)
        post = blog.blogpost_set.get(id=post_id)
        # проверяем, отметил ли данный пользователь пост как прочитанный
        user_id = self.request.user.id
        if post.read.all().filter(id=user_id).exists(): # .get(id=user_id) => исключение
            is_read = True
        else:
            is_read = False
        # проверяем, является ли данный пользователь подписчиком:
        # поле author является pk для Blog, поэтому id у них совпадают:
        is_authenticated = self.request.user.is_authenticated
        if is_authenticated:
            user_id = self.request.user.id
            blog_subscribers = blog.subscribers
            is_subscriber = blog_subscribers.all().filter(id=user_id).exists()
        else:
            is_subscriber = False

        context = {
            'blog': blog,
            'post': post,
            'is_subscriber': is_subscriber,
            'is_read': is_read,
        }

        return context


class SubscribersManager(LoginRequiredMixin, View): # добавляет и удаляет подписчиков
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        blog_id = kwargs['blog_id']
        # поле author является pk для Blog, поэтому id у них совпадают:
        blog = Blog.objects.get(author_id=blog_id)
        blog_subscribers = blog.subscribers
         # если пользователь не подписан, то он добавляется в подписчики
         # если подписан - удаляется. Надпись на кнопке в шаблонах тоже меняется
        if not blog_subscribers.all().filter(id=user_id).exists():
            blog_subscribers.add(user)
        else:
            blog_subscribers.remove(user)
            # удаляем все отметки "прочитано" в соответствии с заданием:
            posts_set = BlogPost.objects.filter(blog=blog)
            for post in posts_set:
                post_read = post.read # список тех, кто отметил пост прочитанным
                if post_read.all().filter(id=user_id).exists():
                    post_read.remove(user)

        # возвращаемся на предыдущую страничку с помощью HTTP_REFERER
        # если HTTP_REFERER отсутствует - на главную:
        previous_url = (request.META.get('HTTP_REFERER', ''))
        return redirect(previous_url)


class MarkRead(LoginRequiredMixin, View): # помечает пост прочитанным
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        post_id = kwargs['post_id']
        post = BlogPost.objects.get(pk=post_id)

        post_read = post.read # список тех, кто отметил пост прочитанным
        post_read.add(user) # если user уже в post_read, то не дублируется

        # возвращаемся на предыдущую страничку с помощью HTTP_REFERER
        # если HTTP_REFERER отсутствует - на главную:
        previous_url = (request.META.get('HTTP_REFERER', ''))
        return redirect(previous_url)


class CreatePost(LoginRequiredMixin, generic.CreateView): # создаёт пост
    # после создания поста инициируется переход на этот пост с помощью
    # instance.get_absolute_url, вызываемого автоматически
    model = BlogPost
    fields = ['title', 'text', 'image', 'pub_date']
    template_name_suffix = '_create_form'

    # привязываем создаваемый пост к блогу текущего пользователя:
    def form_valid(self, form):
        # поле author является pk для Blog, поэтому id у них совпадают:
        blog_id = self.request.user.id
        blog = Blog.objects.get(author_id=blog_id)
        form.instance.blog = blog
        return super().form_valid(form)
