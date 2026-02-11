from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def postteachingjob(request):
    return render(request,'postteachingjob.html')

@login_required(login_url='login')
def admin(request):
    return render(request,'admindashboard.html')