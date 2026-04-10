from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Auth
    path('csrf/', views.csrf_token_view, name='api-csrf'),
    path('auth/login/', views.LoginView.as_view(), name='api-login'),
    path('auth/logout/', views.LogoutView.as_view(), name='api-logout'),
    path('auth/register/', views.RegisterView.as_view(), name='api-register'),
    path('auth/me/', views.MeView.as_view(), name='api-me'),

    # Jobs
    path('jobs/', views.JobListView.as_view(), name='api-jobs'),
    path('jobs/trending/', views.TrendingJobsView.as_view(), name='api-jobs-trending'),
    path('jobs/saved/', views.SavedJobsView.as_view(), name='api-jobs-saved'),
    path('jobs/saved-ids/', views.SavedJobIdsView.as_view(), name='api-jobs-saved-ids'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='api-job-detail'),
    path('jobs/<int:job_id>/save/', views.save_job, name='api-job-save'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='api-job-apply'),

    # Applications
    path('applications/', views.MyApplicationsView.as_view(), name='api-applications'),
    path('applications/<int:job_id>/withdraw/', views.withdraw_application, name='api-withdraw'),

    # Teacher Profile
    path('teacher/profile/', views.TeacherProfileView.as_view(), name='api-teacher-profile'),

    # Schools
    path('schools/', views.SchoolListView.as_view(), name='api-schools'),

    # Metadata
    path('metadata/', views.metadata, name='api-metadata'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
