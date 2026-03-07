from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from.models import SchoolSponsor,SchoolCategory,School
from myutils import *

from django.db.models import Q
# Create your views here.

@login_required(login_url='login')
def schoolsfeed(request):
    schools = School.objects.all()
    schools_page = paginateList(request,list=schools,units_per_page= 20)
    followed_schools = getTeacherFollowedSchools(request)
    context = createContext(request)
    context = context |{'schools_page':schools_page,'followed_schools':followed_schools}
    return render(request,'schoolsfeed.html',context)

@login_required(login_url='login')
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


def followSchool(request,school_id):
    teacher = getTeacherProfile(request)
    school = School.objects.get(id = school_id)
    # teacher_saved_schools = getTeacherSavedJobs()
    teacher.schools_followed.add(school)
    return returnToPrevPage(request)

def searchschools(request):
    context = createContext(request)
    tearm = request.GET.get('tearm')

    return ('schoolsfeed.html',context)