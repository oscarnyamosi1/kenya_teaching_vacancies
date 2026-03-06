from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class Skill(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title


class PaymentCriteria(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class TimeFrameDescriptions(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
    
class Location(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class ExperienceLevel(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Job(models.Model):
    assigner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='this_job_assigner')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.ManyToManyField(Location,blank=True,related_name='this_location_jobs')
    reward = models.PositiveIntegerField(default=0,blank=True)
    posted = models.DateField(auto_now_add=True)
    payment_criteria = models.ManyToManyField(PaymentCriteria,blank=True,related_name = 'this_criteria_jobs')
    experience = models.ManyToManyField(ExperienceLevel,blank=True,related_name='this_experience_level_jobs')
    timeframe = models.ManyToManyField(TimeFrameDescriptions,blank=True,related_name = 'this_timeframedesc_jobs')
    main_field = models.CharField(max_length=50,blank=True,null=True)
    deadline = models.DateTimeField()
    application_slots = models.PositiveIntegerField(default=0,blank=True,null=True)
    skills = models.ManyToManyField(Skill,blank=True,related_name="this_skill_jobs")
    skills2 =[]

    @property
    def getpaymentcriteria(self):
        paymentCriteria  = self.payment_criteria.last()
        return paymentCriteria
    @property
    def gettimeframe(self):
        timeframe  = self.timeframe.last()
        return timeframe
    @property
    def getjobskills (self):
        skills = self.skills.all()
        self.skills2 = skills
        self.save()
        return self.skills2
    @property
    def getjoblocation(self):
        location = self.location.last()
        return location
    
    @property
    def getjobexperience(self):
        experience_level = self.experience.last()
        return experience_level

    hot = 'Hot'
    actively_hiring = 'Actively Hiring'
    new = 'New'

    hiring_state_choices = [(hot,'Hot'),(actively_hiring,'Actively Hiring'),(new,"New")]

    hiring_state = models.CharField(max_length=50,choices=hiring_state_choices,default=new)
    thumbnail = models.ImageField(
        upload_to='jobthumbnails',
        default='jobfallback.webp'
    )
    with_equity = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class SavedJob(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True)
    job = models.ForeignKey(Job,on_delete = models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.user.username +"'s saved job ( " + self.job.title + " ) ."

    

class JobRequirement(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    body = models.CharField(max_length=70,blank=True,null=True)
    
    def __str__(self):
        return self.body
     
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
    skills = models.ManyToManyField(Skill,related_name='this_profile_skills')
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
    
    
class AppliedJob(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True)
    job = models.ForeignKey(Job,on_delete = models.CASCADE,blank=True,null=True)
    is_granted = models.BooleanField(default=False,null=True,blank=True)
    applicant_profile = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)
    
    @property
    def build_applicant_profile(self):
        profile_exists = Profile.objects.filter(user = self.user).exists()
        if profile_exists:
            profile = Profile.objects.get(user = self.user)
            self.applicant_profile = profile 
        else:
            new_profile = Profile.objects.create(user = User)
            self.applicant_profile = new_profile
        self.save()
            
    
    def __str__(self):
        return self.user.username +"'s applied job ( " + self.job.title + " ) ."
 
    
class Account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=00)
    pending_clearance = models.PositiveIntegerField(default=00)
    lifetime_earnings = models.PositiveIntegerField(default=00)
    
    def __str__(self):
        return self.user.username + "'s ."
    
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
    sender = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
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

class Transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    transaction_id = models.CharField(max_length=100)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    released = 'Released'
    pending='Pending'
    refunded = 'Refunded'

    transaction_statuses = [(released,'Released'),(pending,'Pending'),(refunded,'Refunded')]

    status = models.CharField(max_length=50,choices=transaction_statuses,default=pending)

class Assignment(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    doer = models.ForeignKey(User,on_delete=models.CASCADE) 
    assigner = 'oscar'
    is_active = models.BooleanField(default=True)
    is_reviewed = models.BooleanField(default = True)
    
    in_progress = 'In Progress'
    awaiting_review = 'Awaiting Review'
    completed = 'Completed'

    progressChoices = [(in_progress,'In Progress'),(awaiting_review,'Awaiting Review'),(completed,'Completed')]
    progress = models.CharField(default=in_progress,choices=progressChoices)
    date_started = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True,null=True)
    reward = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Assignment for '{self.doer}' given by '{self.assigner}'."
    