from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myutils import *
# Create your views here.
@login_required(login_url='login')
def myapplications(request):
    teacher = getTeacherProfile(request)
    applications = teacher.applied_jobs.all()
    context = createContext(request)
    context = context|{'applications':applications}
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