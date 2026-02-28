from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('myapplications/',views.myapplications,name="myapplications"),
    path('applyjob/',views.applyjob,name='applyjob'),
    path('withdrawapplication/<int:jobid>',views.withdrawapplication,name='withdrawapplication'),
    path('messageschool/<int:application_id>',views.messageschool,name='messageschool'),
    path('messageschool/',views.messageschool,name='messageschool'),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)