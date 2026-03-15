# from django.db import models
# from employers.models import Employer
# # from datetime import date,timedelta
# from django.utils import timezone
# from django.contrib.auth.models import User
# from main.models import *
# from django.urls import reverse

# # Create your models here.



# employment_choices = (
#     ('Full Time','Full Time'),
#     ('Contract','Contract'),
#     ('B.O.M','B.O.M'),
#     ('P.T.A','P.T.A'),
#     ('Substitute','Substitute')
# )
# carriculum_types = (
#     ('IGCSE','IGCSE'),
#     ('8-4-4','8-4-4'),
#     ('J.S.S','J.S.S'),
#     ('E.C.D.E','E.C.D.E'),
#     ('High School','High School')
# )
# class Job(models.Model):
#     employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
#     job_title = models.CharField(max_length=255)
#     job_description = models.CharField(max_length=200,blank=True,null=True)
#     subjects_required = models.ManyToManyField('main.Subject',related_name='jobsubjects')
#     grade_level = models.CharField(max_length=50)
#     min_experience = models.PositiveIntegerField(default=0,blank=True,null=True)
#     tsc_required = models.BooleanField(default=False)
#     carriculum_type = models.CharField(max_length=20,choices=carriculum_types,default='High School')

#     salary_min = models.PositiveIntegerField(blank=True,null=True)
#     salary_max = models.PositiveIntegerField(blank=True,null=True)

#     location = models.CharField(max_length=100)
#     county = models.ForeignKey('main.County',on_delete=models.CASCADE)
#     constituency = models.ForeignKey('main.Constituency',on_delete=models.CASCADE,)
#     specialization_required = models.ForeignKey('main.Specialization',on_delete=models.CASCADE,blank=True,null=True)
#     employment_type = models.ForeignKey('main.EmploymentType',on_delete=models.CASCADE,related_name='jobemploymenttype',null=True)

#     is_promoted = models.BooleanField(default=False)

#     application_deadline = models.DateTimeField()
#     date_posted = models.DateTimeField(auto_now_add=True,blank=True,null=True)

#     is_featured = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
    
#     is_urgent = models.BooleanField(default=False)
#     views = models.PositiveIntegerField(default=0)
#     saves = models.PositiveIntegerField(default=0)

#     total_applications = models.PositiveIntegerField(default=0)
#     applications_reviewed = models.PositiveIntegerField(default=0)

#     is_job = models.BooleanField(default=True)

#     @property
#     def convertSalaryMin(self):
#         if self.salary_min is None:
#             return None
#         else:
#             return self.salary_min//1000

#     @property
#     def convertSalaryMax(self):
#         if self.salary_min is None:
#             return None
#         else:
#             return self.salary_max//1000


#     @property
#     def days_posted(self):
#         now = timezone.now()
#         difference = now-self.date_posted

#         if difference.days == 0:
#             if (difference.seconds//3600) < 2:
#                 return f'{difference.seconds//3600} hr'
#             else:
#                 return f'{difference.seconds//3600} hrs'

#         else:
#             return f'{difference.days + 1} d'

#     @property
#     def days_to_deadline(self):
#         now = timezone.now()
#         difference = self.application_deadline - now
#         if difference.days == 0:
#             if (difference.seconds//3600) < 2:
#                 return f'{difference.seconds//3600} hr'
#             else:
#                 return f'{difference.seconds//3600} hrs'

#         else:
#             return f'{difference.days + 1} d'

#     def __str__(self):
#         return f'''Job {self.job_title}.'''
    






















from django.db import models
from employers.models import Employer
from django.utils import timezone
from main.models import *
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Now

# Choices
employment_choices = (
    ('Full Time','Full Time'),
    ('Contract','Contract'),
    ('B.O.M','B.O.M'),
    ('P.T.A','P.T.A'),
    ('Substitute','Substitute')
)
carriculum_types = (
    ('IGCSE','IGCSE'),
    ('8-4-4','8-4-4'),
    ('J.S.S','J.S.S'),
    ('E.C.D.E','E.C.D.E'),
    ('High School','High School')
)

# Custom QuerySet and Manager for trending
class JobQuerySet(models.QuerySet):
    def trending(self, limit=10):
        # Order by cached trending score for speed
        return self.filter(is_active=True).order_by('-trending_score_cached')[:limit]

class JobManager(models.Manager):
    def get_queryset(self):
        return JobQuerySet(self.model, using=self._db)

    def trending(self, limit=10):
        return self.get_queryset().trending(limit=limit)

# Job model
class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_description = models.CharField(max_length=200, blank=True, null=True)
    subjects_required = models.ManyToManyField('main.Subject', related_name='jobsubjects')
    grade_level = models.CharField(max_length=50)
    min_experience = models.PositiveIntegerField(default=0, blank=True, null=True)
    tsc_required = models.BooleanField(default=False)
    carriculum_type = models.CharField(max_length=20, choices=carriculum_types, default='High School')

    salary_min = models.PositiveIntegerField(blank=True, null=True)
    salary_max = models.PositiveIntegerField(blank=True, null=True)

    location = models.CharField(max_length=100)
    county = models.ForeignKey('main.County', on_delete=models.CASCADE)
    constituency = models.ForeignKey('main.Constituency', on_delete=models.CASCADE)
    specialization_required = models.ForeignKey('main.Specialization', on_delete=models.CASCADE, blank=True, null=True)
    employment_type = models.ForeignKey('main.EmploymentType', on_delete=models.CASCADE, related_name='jobemploymenttype', null=True)

    is_promoted = models.BooleanField(default=False)
    application_deadline = models.DateTimeField()
    date_posted = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_urgent = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    saves = models.PositiveIntegerField(default=0)
    total_applications = models.PositiveIntegerField(default=0)
    applications_reviewed = models.PositiveIntegerField(default=0)
    is_job = models.BooleanField(default=True)

    trending_score_cached = models.FloatField(default=0)  # cached score for fast queries

    objects = JobManager()  # custom manager

    # Salary conversion properties
    @property
    def convertSalaryMin(self):
        if self.salary_min is None:
            return None
        return self.salary_min // 1000

    @property
    def convertSalaryMax(self):
        if self.salary_max is None:
            return None
        return self.salary_max // 1000

    # Days posted / deadline
    @property
    def days_posted(self):
        now = timezone.now()
        difference = now - self.date_posted
        if difference.days == 0:
            hrs = difference.seconds // 3600
            return f'{hrs} hr' if hrs < 2 else f'{hrs} hrs'
        else:
            return f'{difference.days + 1} d'

    @property
    def days_to_deadline(self):
        now = timezone.now()
        difference = self.application_deadline - now
        if difference.days == 0:
            hrs = difference.seconds // 3600
            return f'{hrs} hr' if hrs < 2 else f'{hrs} hrs'
        else:
            return f'{difference.days + 1} d'

    # Per-instance trending score
    @property
    def trending_score(self):
        now = timezone.now()
        hours_since_posted = (now - self.date_posted).total_seconds() / 3600
        hours_since_posted = max(hours_since_posted, 1)

        # Engagement
        engagement_score = self.views * 1 + self.saves * 3 + self.total_applications * 5

        # Boosts
        boost = 0
        if self.is_featured:
            boost += 20
        if self.is_promoted:
            boost += 15
        if self.is_urgent:
            boost += 10

        # Freshness
        if hours_since_posted <= 24:
            boost += 25
        elif hours_since_posted <= 72:
            boost += 15
        elif hours_since_posted <= 168:
            boost += 5

        # Velocity & application rate
        velocity_score = self.views / hours_since_posted * 2
        application_rate_score = self.total_applications / hours_since_posted * 2

        score = engagement_score + boost + velocity_score + application_rate_score
        return round(score, 2)

    def __str__(self):
        return f"Job {self.job_title}."