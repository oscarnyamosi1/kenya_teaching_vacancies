from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from . import views,jobstuff,teacherstuff,schoolstuff
urlpatterns = [
    # Auth    
    path('auth/login/',views.login_view,name="login"),
    path('auth/logout/', views.logout_view, name='api-logout'),
    path('auth/me/', views.me_view, name='api-me'),

    path('refresh/', views.refresh_view),
    path('auth/refresh/', views.refresh_view),

    path('jobs/', jobstuff.getJobList),
    path('jobs/saved/',jobstuff.getSavedJobs),

    path('jobs/checkJobSavedStatus/',jobstuff.checkJobSavedStatus),
    path('jobs/checkJobAppliedStatus/',jobstuff.checkJobAppliedStatus),

    path('jobs/<int:jobId>/save/',jobstuff.saveJob),
    path('jobs/<int:jobId>/unsave/',jobstuff.unsaveJob),
    
    path('jobs/applications/',jobstuff.getMyApplications),
    path('jobs/<int:jobId>/apply/',jobstuff.applyJob),

    path('jobs/applications/<int:jobId>/withdraw/',jobstuff.deleteApplication),
    path('jobs/jobdetail/<int:savedId>/',jobstuff.viewJob),

    path('schools/',schoolstuff.getSchools),
    path('schools/follow/',schoolstuff.followSchool),

    path('schools/unfollow/',schoolstuff.unfollowSchool),
    path('schools/checkFollow/',schoolstuff.checkFollow),

    path('teacher/profile/', teacherstuff.getTeacherProfile),

    # Jobs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
