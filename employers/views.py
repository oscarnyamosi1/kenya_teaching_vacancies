from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from myutils import createContext

# Create your views here.
@login_required(login_url='login')
def postteachingjob(request):
    context=createContext(request)
    return render(request,'postteachingjob.html',context)

@login_required(login_url='login')
def admin(request):
    context=createContext(request)
    return render(request,'admindashboard.html',context)