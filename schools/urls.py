from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('schoolsfeed/',views.schoolsfeed,name='schoolsfeed'),
    path('blog',views.blog,name='blog'),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)