from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class SchoolCategory(models.Model):
    title = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return f'''{self.title.capitalize()}'''
    

class SchoolSponsor(models.Model):
    title = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return f'''{self.title.upper()}'''
    


class School(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True,unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    school_type = models.ForeignKey('schools.SchoolSponsor',on_delete=models.CASCADE,blank=True,null=True)
    category = models.ForeignKey(SchoolCategory,on_delete=models.CASCADE,blank=True,null=True)
    
    logo = models.ImageField(upload_to='schoollogos/',blank=True,null=True)
    is_school = models.BooleanField(default=True)
    establishment_year = models.DateTimeField(blank=True,null=True)

    is_school = models.BooleanField(default=True)

    def __str__(self):
        return f'''{self.name.capitalize()}.'''

class SchoolBlog(models.Model):
    school = models.ForeignKey('schools.School',on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=100,blank=True,null=True)
    media_form_history = models.FileField(upload_to=f'schoolhistorys/', max_length=100)
    text_history = models.TextField()
    history_summary = models.TextField(blank=True,null=True)
    posted_on = models.DateTimeField(blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='school_blogs')
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated tags for the blog post.")
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft')
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.school.name}'s Blog."
