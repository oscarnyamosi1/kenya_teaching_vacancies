from django.shortcuts import render,redirect
from django.contrib import auth,messages
from .models import *
from jobs.views import createContext
from jobs.models import Job
from django.contrib.auth.models import User
from applications.models import Application
from myutils import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import IntegrityError
from messagesapp.models import Profile,Inbox,Sentbox


@login_required(login_url='login')
def home(request):
    context = maincontext(request)

    # create profile
    # create inbox
    # create sentbox
    teacher = getTeacherProfile(request)

    try:
        teacher_profile = Profile.objects.create(user = teacher)
        teacher_inbox = Inbox.objects.create(user = teacher)
        teacher_sentbox = Inbox.objects.create(user = teacher)

        teacher_profile.save()
        teacher_inbox.save()
        teacher_sentbox.save()
    except IntegrityError:
        pass

    # createCountynConstituencies()
    all_jobs = context.get('all_jobs', [])
    promoted_jobs=Job.objects.filter(is_promoted=True)
    jobs_page = paginateList(request,list=all_jobs,units_per_page=20)
    context = context | {'jobs_page':jobs_page,"promoted_jobs":promoted_jobs}
    return render(request, "index.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            email_exists = User.objects.filter(email = email).exists()
            if password == "" or (password.__len__() < 8):
                print("------------------------> Password too short")
                messages.info(request,"message too schort")
                context = {'email':email}
                return redirect('login')
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
    try:
        step = request.GET.get('q')
        if int(step )== 1:
            pass
    except:
        pass
    
   
    return render(request,'signupflow.html')

def blog(request):
    return render(request,'->blog.html')

def errorr(request):
    return render (request,'500.html')

def searchSite(request):
    args = request.GET.get('q')
    result = Job.objects.filter(
        Q(job_title__icontains = args)|
        Q(job_description__icontains = args)
               )
    jobs_feed_page = paginateList(request,result,10)
    context = createContext(request)|{'jobs_feed_page':jobs_feed_page}
    return render(request,'jobfeed.html',context)


# communications pages

from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, 'index.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def pricing(request):
    return render(request, 'pricing.html')

def contact(request):
    return render(request, 'contact.html')

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # TODO: process message (save to DB or send email)
        return HttpResponseRedirect(reverse('contact'))
    return HttpResponseRedirect(reverse('contact'))