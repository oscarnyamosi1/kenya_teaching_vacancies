from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('teacherprofile/',views.teacherprofile,name='teacherprofile'),
    path('teacherfeed/',views.teacherfeed,name='teacherfeed'),
    path('profilesettings/',views.profilesettings,name='profilesettings'),
    path("notifications/", views.notifications, name="notifications"),
    path('settings/',views.settings,name='settings'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('createteacherprofile/',views.editprofile,name='editprofile'),
    path('uploaddocuments/',views.uploaddocuments,name='uploaddocuments')
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)