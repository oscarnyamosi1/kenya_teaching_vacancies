from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('blog/',views.blog,name='blog'),
    path('errorr/',views.errorr,name='errorr'),

    
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('pricing/', views.pricing, name='pricing'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),  # Form submission
    path('search/',views.searchSite,name='searchsite')
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)