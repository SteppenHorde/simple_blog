from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import generic, View
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect

from .models.blog import Blog, BlogPost



class Main(TemplateView):
    template_name = 'core/main.html'
    """
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        #return render(request, self.template_name, context=context)
        return context
    """


class Blogs(TemplateView):
    template_name = 'core/blogs.html'

    def get_context_data(self, *args, **kwargs):
        all_blogs_query_set = Blog.objects.all()
        all_blogs_set = set()

        if self.request.user.is_authenticated:
            is_authenticated = True
            user_id = self.request.user.id
            user = User.objects.get(id=user_id)
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


class ShowBlog(TemplateView):
    template_name = 'core/show_blog.html'

    def get_context_data(self, *args, **kwargs):
        blog_id = kwargs['blog_id']
        # поле author является pk для Blog, поэтому id у них совпадают:
        blog = Blog.objects.get(author_id=blog_id)
        posts_list = blog.blogpost_set.all()

        # проверяем, является ли данный пользователь подписчиком:
        # поле author является pk для Blog, поэтому id у них совпадают:
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            user = User.objects.get(id=user_id)
            blog_subscribers = blog.subscribers
            is_subscriber = blog_subscribers.all().filter(id=user_id).exists()
        else:
            is_subscriber = False

        context = {
            'blog': blog,
            'posts_list': posts_list,
            'is_subscriber': is_subscriber,
        }

        return context


class ShowPost(TemplateView):
    template_name = 'core/show_post.html'

    def get_context_data(self, *args, **kwargs):
        blog_id = kwargs['blog_id']
        post_id = kwargs['post_id']
        # поле author является pk для Blog, поэтому id у них совпадают:
        blog = Blog.objects.get(author_id=blog_id)
        post = blog.blogpost_set.get(id=post_id)

        # проверяем, является ли данный пользователь подписчиком:
        # поле author является pk для Blog, поэтому id у них совпадают:
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            user = User.objects.get(id=user_id)
            blog_subscribers = blog.subscribers
            is_subscriber = blog_subscribers.all().filter(id=user_id).exists()
        else:
            is_subscriber = False

        context = {
            'blog': blog,
            'post': post,
            'is_subscriber': is_subscriber,
        }

        return context


class SubscribersManager(View):
    def post(self, request, *args, **kwargs):
        template_name = 'core/show_post.html'
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

        return redirect(reverse('main'))


class CreatePost(generic.CreateView):
    pass
    #form_class = UserCreationForm
    #success_url = reverse_lazy('login') # после создания поста переход на
    #template_name = 'core/create_post.html'
