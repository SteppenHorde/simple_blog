from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import generic, View

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
        all_blogs_set = Blog.objects.all()
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

        context = {
            'blog': blog,
            'posts_list': posts_list,
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

        context = {
            'blog': blog,
            'post': post,
        }

        return context


class SubscribersManager(View):
    pass
    #def post(self, request, *args, **kwargs):
        #print(args)
        #print(kwargs)


class CreatePost(generic.CreateView):
    pass
    #form_class = UserCreationForm
    #success_url = reverse_lazy('login') # после создания поста переход на
    #template_name = 'core/create_post.html'
