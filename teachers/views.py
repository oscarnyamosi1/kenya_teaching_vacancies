from django.shortcuts import render,redirect
from main.views import createContext
from django.contrib.auth.decorators import login_required
from .models import *
from myutils import *
# Create your views here.

@login_required(login_url='login')
def teacherprofile(request):
    this_teacher_exists = Teacher.objects.filter(user = request.user ).exists()
    if this_teacher_exists :
        this_teacher = Teacher.objects.get(user = request.user )
    else:
        this_teacher = None
    context = createContext(request)
    context2 = {'teacher':this_teacher}
    context = context|context2
    return render(request,'teacherprofile.html',context)

@login_required(login_url='login')
def profilesettings(request):
    return render(request,'profilesettings.html')

@login_required(login_url='login')
def messages(request):
    return render(request,'teachermessages.html')

@login_required(login_url='login')
def notifications(request):
    return render(request,'notifications.html')


@login_required(login_url='login')
def settings(request):
    return render(request,"settings.html")

@login_required(login_url='login')
def editprofile(request):
    return render(request,'editprofile.html')

@login_required(login_url='login')
def uploaddocuments(request):
    return render(request,'uploaddocuments.html')

@login_required(login_url='login')
def createteacherprofile(request):
    return redirect('editprofile')

def teacherfeed(request):
    teachers = Teacher.objects.all()
    context = {'teachers':teachers}
    return render(request,'teacherfeed.html',context)

