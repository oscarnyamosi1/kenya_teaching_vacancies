from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from teachers.models import Teacher
from django.db.models import Q
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
from applications.models import Application
from myutils import *
import random
from schools.models import School
from main.models import County,Constituency


@login_required(login_url='login')
def savedjobs(request):
    context = createContext(request)
    savedjobs =  getTeacherSavedJobs(request).order_by('-id')
    units_per_page = 10
    condition = f'savedjobs > {units_per_page} '
    saved_jobs_page = paginateList(request,list = savedjobs,units_per_page=units_per_page)
    context = context | {"saved_jobs_page": saved_jobs_page,'condition':condition}
    return render(request, "savedjobs.html", context)



def jobfeed(request):
    context = createContext(request)
    alljobs = context.get('all_jobs',[])
    jobs_feed_page = paginateList(request,list=alljobs,units_per_page=20)
    context = context | {'jobs_feed_page':jobs_feed_page}
    return render(request,'jobfeed.html',context)

@login_required(login_url='login')
def postjob(request):
    return render(request,'postteachingjob.html')

@login_required(login_url='login')
def premiumurgent(request):
    return render(request,"premiumpricing.html")

@login_required(login_url='login')
def savejob(request,jobid):
    from main.views import getTeacherProfile,getJobById
    job = getJobById(jobid)
    if job is not None:
        teacher = getTeacherProfile(request)
        teacher.saved_jobs.add(job)
        teacher.save()
    else:
        messages.info(request,"Job doesn't exist !",extra_tags='warning')
    return returnToPrevPage(request)


def search(request,filter='',page_no=None):
    context = createContext(request)
    tearm = request.GET.get('jobquery','')

    def searchLocations():
        locations = County.objects.filter(
            Q(title__icontains=tearm)
        ).order_by('title')
        jobs_frm_locations = []
        for location in locations:
            jobs = list(Job.objects.filter(county = location))
            jobs_frm_locations.extend(jobs)
        
        return jobs_frm_locations
    def searchSchools():
        schools = School.objects.filter(
            Q(name__icontains = tearm)
        ).order_by('-id')
        

        school_employers = []
        for school in schools:
            school_employers_small = list(Employer.objects.filter(school = school))
            school_employers.extend(school_employers_small)
       
        jobs_frm_schools = []
        for employer in school_employers:
            jobs = list(Job.objects.filter(employer = employer ))
            jobs_frm_schools.extend(jobs)
        return jobs_frm_schools
    def searchSubjects():
        subjects = Subject.objects.filter(
            Q(title__icontains = tearm)
        ).order_by('-id')

        subject_jobs = []
        for subject in subjects:
            jobs_per_subject= list(Job.objects.filter(subjects_required = subject))
            subject_jobs.extend(jobs_per_subject)
        return subject_jobs
        
    def searchTitles():
        jobs = Job.objects.filter(
            Q(job_title__icontains = tearm)|
            Q(job_description__icontains = tearm)
        ).order_by('-id')
        return jobs
    
    def searchSchools():
        schools = School.objects.filter(
            Q(name__icontains = tearm)
        )

        print(f'school results {schools}')
        print(f'school results {schools}')
        # find employers to link us to jobs due to their common relationship(employer->job->school)
        school_employers = []

        # one must be an employer in order to post a job (or become an employer automatically once he posts a job) hence this may get broken as the prints will reveal

        for school in schools:
            small_school_employers = list(Employer.objects.filter(school = school))
            school_employers+=small_school_employers

        print(f'school employers --> {school_employers}')
        print(f'school employers --> {school_employers}')


        jobs = []
        for employer in school_employers:
            small_jobs = list(Job.objects.filter(employer = employer))

            print(f'school small_jobs {small_jobs}')
            print(f'school small_jobs {small_jobs}')

            jobs.extend(small_jobs)
            
        print(f'school jobs {jobs}')
        print(f'school jobs {jobs}')
        return jobs
    # profile_based_results = []

    if filter == '':
        r1 = searchLocations()
        r2 = searchSchools()
        r3 = searchSubjects()
        r4 = searchTitles()
        r5 = searchSchools()

        results = list(chain(r1,r2,r3,r4,r5))
    elif filter == 'location':
        results = searchLocations()
    elif filter == 'school' :
        results = searchSchools()
    elif filter == 'subject':
        results = searchSubjects()
    elif filter == 'title':
        results = searchTitles()
    else:
        r1 = searchLocations()
        r2 = searchSchools()
        r3 = searchSubjects()
        r4 = searchTitles()
        r5 = searchSchools()

        results = list(chain(r1,r2,r3,r4,r5))

    # else:
    #     return redirect('home')
    try:
        if page_no == None:
            search_page = paginateList(request,list=results,units_per_page= 10)
        else:
            search_page = paginateList(request,list=results,units_per_page= 10,page=int(page_no))

        context = context|{'search_page':search_page}

        return render(request,'searchresults.html',context)
    except UnboundLocalError or ValueError:
        # search(request,filter = 'location')
        return HttpResponse('Error while searching')
    
    

@login_required(login_url='login')
def applyjob(request,jobid):
    job_to_apply = Job.objects.get(id=jobid)
    teacher = getTeacherProfile(request)

    # from main.views import getAllJobsApplied
    my_applications = getAllJobsApplied(request)
  
    if job_to_apply in my_applications:
        messages.info(request,'You already applied for this job !')
    else:
        teacher.applied_jobs.add(job_to_apply)
    return returnToPrevPage(request)


@login_required(login_url='login')
def withdrawsave(request,jobid):
    job = getJobById(jobid)
    teacher = getTeacherProfile(request)
    teacher.saved_jobs.remove(job)
    return returnToPrevPage(request)
def sharejob(request,jobid):
    return HttpResponse("Sharing job.")