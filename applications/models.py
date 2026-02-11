from django.db import models
from django.contrib.auth.models import User

from jobs.models import Job
from teachers.models import Teacher
from employers.models import Employer
# Create your models here.

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    approver = models.ForeignKey(Employer,on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Applied', 'Applied'),
            ('Shortlisted', 'Shortlisted'),
            ('Interview', 'Interview'),
            ('Rejected', 'Rejected'),
        ],
        default='Applied'
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'''Application {self.job.job_title}.'''
    