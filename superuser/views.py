from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myutils import createContext
# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    context = createContext(request)
    return render(request,'sudashboard.html',context)