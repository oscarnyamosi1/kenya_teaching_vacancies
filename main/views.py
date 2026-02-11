from django.shortcuts import render,redirect
from django.contrib import auth,messages
from .models import *
from jobs.views import createContext
from jobs.models import Job
from django.contrib.auth.models import User
from applications.models import Application
from myutils import *
from django.contrib.auth.decorators import login_required



# from .models import createConstituencies,createCounties
# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    context = maincontext(request)
    createCountynConstituencies()
    all_jobs = context.get('all_jobs', [])
    paginator = Paginator(all_jobs, 50)
    page_number = request.GET.get('page')
    try:
        jobs_page = paginator.page(page_number)
    except PageNotAnInteger:
        jobs_page = paginator.page(1)
    except EmptyPage:
        jobs_page = paginator.page(paginator.num_pages)
    context['jobs_page'] = jobs_page
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

