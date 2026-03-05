from django.shortcuts import render,redirect
from django.contrib import auth,messages
from .models import *
from jobs.views import createContext
from jobs.models import Job
from django.contrib.auth.models import User
from applications.models import Application
from myutils import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    context = maincontext(request)
    # createCountynConstituencies()
    all_jobs = context.get('all_jobs', [])
    # all_jobs = Job.objects.all()
    promoted_jobs=Job.objects.filter(is_promoted=True)
    print(f"""
    
    all jobs {all_jobs[0:10]}
    
""")
    jobs_page = paginateList(request,list=all_jobs,units_per_page=20)
    context = context | {'jobs_page':jobs_page,"promoted_jobs":promoted_jobs}
    return render(request, "index.html", context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        email_exists = User.objects.filter(email = email).exists()
        if password == "" or (password.__len__() < 8):
            print("------------------------> Password too short")
        else:
            if email_exists: 
                username = User.objects.get(email = email).username
                user = auth.authenticate(request,username = username,password=password)

                auth.login(request,user)
                return redirect("home")
            else:
                messages.info(request,'Wrong credentials')
                print("Email doesn't exist")

    return render(request,'loginpage.html')


def logout(request):
    auth.logout(request)
    return redirect("login")

def signup(request):
   
    return render(request,'signupflow.html')

def blog(request):
    return render(request,'->blog.html')

