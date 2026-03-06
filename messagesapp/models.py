from django.db import models
from django.contrib.auth.models import User
from datetime import date


# from teachers.models import Teacher
# from employers.models import Employer

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    content = models.TextField()
    receiver = models.ForeignKey("teachers.Teacher",on_delete=models.CASCADE,related_name="received_messages",null=True)

    def __str__(self):
        return f"{self.content[0:10]}"

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    profile_pic_uploaded = models.BooleanField(default=False)
    birthday = models.DateField(blank=True,null=True)
    picture = models.ImageField(
        upload_to='profilepics',
        default='fallback.jpg'
    )
    joined = models.DateTimeField(auto_now_add=True)
    @property
    def age(self):
        today = date.today()
        age = today.year - self.birthday.year-((today.month,today.day)<(self.birthday.month,self.birthday.day))
        return age
    
    @property
    def timeactive(self):
        today = date.today()
        active_time = today.year - self.joined.year-((today.month,today.day)<(self.joined.month,self.joined.day))
        return active_time

    def __str__(self):
        return self.user.username + "'s Profile."
    
    

class Inbox(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)

    @property 
    def makeInboxProfile(self):
        profile_exists = Profile.objects.filter(user = self.user).exists()
        if profile_exists:
            profile = Profile.objects.get(user = self.user)
            self.profile = profile
            self.save()
        else:
            new_profile = Profile.objects.create(user = self.user)
            new_profile.save()
            return self.makeInboxProfile()


    def __str__(self):
        return self.user.username +"'s inbox."
    
class Sentbox(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    inbox = models.ForeignKey(Inbox,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.user.username +"'s sentbox."
class Message(models.Model):
    sender = models.ForeignKey(Teacher,on_delete=models.CASCADE,blank=True,null=True)
    inbox = models.ForeignKey(Inbox,on_delete=models.CASCADE,blank=True,null=True)
    sentbox = models.ForeignKey(Sentbox,on_delete=models.CASCADE,blank=True,null=True)
    
    body = models.TextField()
    sender_profile = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)
    time_sent = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    @property
    def short_time_sent(self):
        return self.time_sent.time
        
    @property 
    def makeSenderProfile(self):
        profile_exists = Profile.objects.filter(user = self.sender).exists()
        if profile_exists:
            profile = Profile.objects.get(user = self.sender)
            self.sender_profile = profile
            self.save()
        else:
            new_profile = Profile.objects.create(user = self.sender)
            new_profile.save()
            return self.makeSenderProfile()

            
    def __str__(self):
        return self.body[0:40]
    