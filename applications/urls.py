from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('myapplications/',views.myapplications,name="myapplications"),
    path('applyjob/',views.applyjob,name='applyjob'),
    path('withdrawapplication/<int:jobid>',views.withdrawapplication,name='withdrawapplication')
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)