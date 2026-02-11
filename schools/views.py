from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from.models import SchoolSponsor,SchoolCategory,School
from myutils import *
# Create your views here.

def schoolsfeed(request):
    schools = School.objects.all()
    context = createContext(request)
    context = context |{'schools':schools}
    return render(request,'schoolsfeed.html',context)

def blog(request):
    context = createContext(request)
    posts = getAllSchools(request)
    context = context | {'posts':posts}
    return render(request,'blog.html',context)

schoolsponsors = ['international',"public","private","sponsored","Specialneeds",'Other']
school_categories = ('Secondary','Primary','J.S.S','E.C.D.E')
def createschoolsponsor():
    if len(SchoolSponsor.objects.all()) == 0:
        for sponsor in schoolsponsors:
            new_sponsor = SchoolSponsor.objects.create(title = sponsor)
            new_sponsor.save()
def createschoolcategory():
    if len(SchoolCategory.objects.all()) == 0:
        for category in school_categories:
            new_category = SchoolCategory.objects.create(title = category)
            new_category.save()