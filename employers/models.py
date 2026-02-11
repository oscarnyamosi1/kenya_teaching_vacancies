from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User



# county_choices = (("kisii","kisii"),("nairobi","nairobi"))

class Employer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.OneToOneField('schools.School', on_delete=models.CASCADE,null=True,blank=True)
    employer_location = models.ForeignKey('main.County',on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'''Employer {self.user.username}.'''
    