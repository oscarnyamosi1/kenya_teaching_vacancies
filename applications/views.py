from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myutils import *
from employers.models import Employer
from applications.models import Application,ApplicationResponse
# Create your views here.
@login_required(login_url='login')
def myapplications(request):
    teacher = getTeacherProfile(request)
    applications = teacher.applied_jobs.all().order_by('-id')
    applications_page = paginateList(request,list=applications,units_per_page=10)
    context = createContext(request)
    context = context|{'applications_page':applications_page,'applications':applications}
    return render(request,'myapplications.html',context)

@login_required(login_url='login')
def applyjob(request):
    return render(request,"applyjob.html")

@login_required(login_url='login')
def withdrawapplication(request,jobid):
    job = getJobById(jobid)
    teacher = getTeacherProfile(request)
    teacher.applied_jobs.remove(job)
    return returnToPrevPage(request)
    
@login_required(login_url='login')
def messageschool(request,application_id):
    applied_jobs =  getAllJobsApplied(request)
    job_application = applied_jobs.get(id=application_id)
    print(f'''

        Job application :{job_application}
        employer : {job_application.employer}
        school :{job_application.employer.school}
          
          ''')
    employer = job_application.employer
    school = employer.school
    applicant = getTeacherProfile(request)

    application_responses = ApplicationResponse.objects.filter(employer=employer,applicant=applicant)
    
    context = createContext(request)
    context = context|{'open_chat':school,'responses':application_responses,'application_id':application_id}
    return render(request,'teachermessages.html',context)