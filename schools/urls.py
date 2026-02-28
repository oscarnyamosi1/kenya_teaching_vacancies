from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('schoolsfeed/',views.schoolsfeed,name='schoolsfeed'),
    path('blog',views.blog,name='blog'),
    path('follow/<int:school_id>',views.followSchool,name = 'follow'),
    path('searchschools/',views.searchschools,name='searchschools'),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)