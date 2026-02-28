from django.db import models
from django.contrib.auth.models import User


# from teachers.models import Teacher
# from employers.models import Employer

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    content = models.TextField()
    receiver = models.ForeignKey("teachers.Teacher",on_delete=models.CASCADE,related_name="received_messages",null=True)

    def __str__(self):
        return f"{self.content[0:10]}"
