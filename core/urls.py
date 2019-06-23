from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views



urlpatterns = [
    path('', views.Main.as_view(), name='main'), # тут будет персональная лента
    path('blogs/', views.Blogs.as_view(), name='blogs'), # все блоги
    path('blogs/<int:blog_id>', views.ShowBlog.as_view(), name='show_blog'),
    path('blogs/<int:blog_id>/(un)subscribe', views.SubscribersManager.as_view(), name='(un)subscribe'),
    path('blogs/<int:blog_id>/create', views.CreatePost.as_view(), name='create_post'),
    path('blogs/<int:blog_id>/<int:post_id>', views.ShowPost.as_view(), name='show_post'),
    path('blogs/<int:blog_id>/<int:post_id>/mark_read', views.MarkRead.as_view(), name='mark_read'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
