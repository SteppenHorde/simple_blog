from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
