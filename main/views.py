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
                # context = {'email':email}
                return redirect('login')
            else:
                if email_exists: 
                    username = User.objects.get(email = email).username
                    user = auth.authenticate(request,username = username,password=password)
                    
                    if user is not None:
                        auth.login(request,user)
                        return redirect("home")
                    else:
                        # alert in javascript wrong password or email
                        return redirect('login')

                else:
                    messages.info(request,'Wrong credentials')
                    print("Email doesn't exist")

        return render(request,'loginpage.html')


def logout(request):
    auth.logout(request)
    return redirect("login")


def signup(request):

    # step = request.GET.get('q', '1')

    if request.method == "POST":

        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone-number')
        teachingFocus = request.POST.get('teaching-focus')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        bio = request.POST.get('bio')
        openToRemoteWork = request.POST.get('open2remote')

        print(f'''
        
        fullname:{fullname}
        email:{email}
        phone:{phone}
        teachingFocus:"{teachingFocus}"
                opentoremote:"{openToRemoteWork}"
                password:"{password}"
                bio "{bio}"
        
        ''')

        # validate passwords
        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('/signup/?q=1')

        # check existing email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('/signup/?q=1')

        # create username automatically
        username = email.split("@")[0]
        messages.info(request,'*Important* Your username is your email name before the @ sign !')

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # store extra info in session for step 2
            # request.session['signup_data'] = {
            #     "fullname": fullname,
            #     "phone": phone,
            #     "bio": bio
            # }

            # # move to next step
        auth.login(request,user)
        return redirect('/teachers/uploaddocuments/')

    # # STEP 1: CREATE ACCOUNT
    # if step == '1':

    return render(request, 'signupflow.html')



    # # STEP 2: DOCUMENT VERIFICATION
    # elif step == '2':

    #     if request.method == "POST":

    #         id_number = request.POST.get("id_number")
    #         tsc_number = request.POST.get("tsc_number")

    #         data = request.session.get("signup_data")

    #         # Here you would save to a profile model
    #         # TeacherProfile.objects.create(...)

    #         messages.success(request, "Account created successfully")

    #         return redirect("/login/")

    #     return render(request, 'signup_documents.html', {"step": 2})


    return render(request, 'signupflow.html')


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


# communications 

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
@login_required(login_url='login')
def changeTheme(request):
    teacher = getTeacherProfile(request)
    requestedtheme = request.GET.get('q')
    if Theme.objects.count() > 0:
        newtheme_exists = Theme.objects.filter(title=requestedtheme).exists()
        if newtheme_exists:
            newtheme = Theme.objects.get(title=requestedtheme)
        else:
            createThemes([requestedtheme])
            newtheme = Theme.objects.get(title=requestedtheme)
            # newtheme = Theme.objects.get(title='macglass')

        teacher.theme = newtheme
        teacher.save()
        return returnToPrevPage(request)
    else:
        createThemes(themeList)
        return returnToPrevPage(request)