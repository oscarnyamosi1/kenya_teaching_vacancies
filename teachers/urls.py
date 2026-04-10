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
    path('uploaddocuments/',views.uploaddocuments,name='uploaddocuments'),
    
    path("account/", views.account_settings, name="account_settings"),
    path("privacy/", views.privacy_settings, name="privacy_settings"),
    path("documents/", views.documents_settings, name="documents_settings"),
    path("notifications/", views.notifications_settings, name="notifications_settings"),
    path("appearance/", views.appearance_settings, name="appearance_settings"),
    path("language/", views.language_settings, name="language_settings"),
    path("help/", views.help_settings, name="help_settings"),
    
    path('change-number/',views.changeNumber,name="change-number"),
    path('change-password/',views.changePassword,name="change-password"),
    path('change-email/',views.changeEmail,name='change-email'),
    path('view-documents/',views.viewDocuments,name='view-documents'),


] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)