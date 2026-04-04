from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myutils import *
from .models import *

# Create your views here.
def createChatParties(request):
    chatparties = []
    inbox = Inbox.objects.get(user = getTeacherProfile(request))
    messages = Message.objects.filter(inbox = inbox)
    for message in messages:
        if message.sender_profile not in chatparties:
            chatparties.append(message.sender_profile)
    
    return chatparties


@login_required(login_url='login')
def teachermessages(request):
    context = createContext(request)
    chatparties = createChatParties(request)

    context = context|{'inboxitems':chatparties}
    return render(request,'teachermessages.html',context)


def selectChat(request):
    pass
