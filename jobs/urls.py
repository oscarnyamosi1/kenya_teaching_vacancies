from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('savedjobs/',views.savedjobs,name='savedjobs'),
    path('sharejob/<int:jobid>/',views.sharejob,name='sharejob'),
    path('jobfeed/',views.jobfeed,name="jobfeed"),
    path('postjob/',views.postjob,name='postjob'),
    path('savejob/<int:jobid>',views.savejob,name='savejob'),
    path('search/',views.search,name='search'),
    path('search/?page=<int:page_no>/',views.search,name='search'),
    path('premiumurgent/',views.premiumurgent,name='premiumurgent'),
    path('applyjob/<int:jobid>',views.applyjob,name='applyjob'),
    path('withdrawsave/<int:jobid>/',views.withdrawsave,name='withdrawsave')
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)