from django.shortcuts import render,redirect
from main.views import createContext
from django.contrib.auth.decorators import login_required
from .models import *
from myutils import *
from django.contrib import messages 

# Create your views here.

@login_required(login_url='login')
def teacherprofile(request):
    from myutils import getTeacherDocuments

    this_teacher_exists = Teacher.objects.filter(user = request.user ).exists()
    if this_teacher_exists :
        this_teacher = Teacher.objects.get(user = request.user )
    else:
        this_teacher = None

    teacherDocuments = getTeacherDocuments(request)
    teacherDocument4json = list(TeacherDocument.objects.filter(teacher = this_teacher).values())

    context = createContext(request)
    context2 = {'teacher':this_teacher,'teacherDocuments':teacherDocuments,'teacherDocument4json':teacherDocument4json}
    context = context|context2
    return render(request,'teacherprofile.html',context)

@login_required(login_url='login')
def profilesettings(request):
    context = createContext(request)
    return render(request,'profilesettings.html',context)

@login_required(login_url='login')
def notifications(request):
    context = createContext(request)
    return render(request,'notifications.html',context)


@login_required(login_url='login')
def settings(request):
    context = createContext(request)
    return render(request,"settings.html",context)

@login_required(login_url='login')
def editprofile(request):
    context = createContext(request)
    return render(request,'editprofile.html',context)

@login_required(login_url='login')
def uploaddocuments(request):
    def filterTeacherDocumentExistance(teacherr,document_type:str):

        def checkExistance(document_type):
            return TeacherDocument.objects.filter(teacher = teacherr,document_type = document_type).exists()

        if document_type == 'National ID':
            return checkExistance(document_type)
        elif document_type == 'Degree Certificate':
            return checkExistance(document_type)
        elif document_type == 'Other Document':
            return checkExistance(document_type)
        elif document_type == 'Carriculum Vitae':
            return checkExistance(document_type)
        elif document_type == 'TSC Certificate':
            return checkExistance(document_type)
        elif document_type == '':
            return checkExistance(document_type)
    teacher = getTeacherProfile(request)
    
    context = createContext(request)
    context2 = {
        'national_id_exists':filterTeacherDocumentExistance(teacher,'National ID'),
        'academic_certificates_exists':filterTeacherDocumentExistance(teacher,'Degree Certificate'),
        'internship_letter_exists':filterTeacherDocumentExistance(teacher,'Other Document'),
        'carriculum_vitae_exists':filterTeacherDocumentExistance(teacher,'Carriculum Vitae'),
        'tsc_certificate_exists':filterTeacherDocumentExistance(teacher,'TSC Certificate')
    }
    context = context | context2
    if request.method == 'POST':


        national_id = request.FILES.get('national-id')
        academic_certificates = request.FILES.get('academic-certificates')
        internship_letter = request.FILES.get('tp-letter')
        carriculum_vitae = request.FILES.get('carriculum-vitae')
        tsc_certificate = request.FILES.get('tsc-certificate')

        # for national id
        if national_id:
            try:
                if TeacherDocument.objects.filter(teacher=teacher,document_type = 'National ID').exists():
                    pass
                else:
                    TeacherDocument.objects.create(teacher = teacher,document_type = 'National ID',file = national_id)
            except:
                print('Error creating national ID')
        else:
            messages.info(request,'Please upload national ID or any missing Document.')
        # for academic certificates
        if academic_certificates:
            try:
                if TeacherDocument.objects.filter(teacher = teacher,document_type = 'Degree Certificate').exists():
                    pass
                else:
                    TeacherDocument.objects.create(teacher=teacher,document_type = 'Degree Certificate',file = academic_certificates)

            except:
                print('Error creating academic certificate.')
        else:
            messages.info(request,'Please upload national Academic Certificates.')

        #for internship letter
        if internship_letter:
            try:
                if TeacherDocument.objects.filter(teacher = teacher,document_type = 'Other Document').exists():
                    pass
                else:
                    TeacherDocument.objects.create(teacher = teacher,document_type = 'Other Document',file = internship_letter)

            except:
                print('Error creating "Other" Document .')
        else:
            messages.info(request,'Please upload internship letter.')
        # for cv 
        if carriculum_vitae:
            try:
                if TeacherDocument.objects.filter(teacher = teacher,document_type = 'Carriculum Vitae').exists():
                    pass
                else:
                    TeacherDocument.objects.create(teacher = teacher,document_type = 'Carriculum Vitae',file = carriculum_vitae)
            except:
                print('Error creating Carriculum Vitae .')
        else:
            messages.info(request,'Please upload carriculum vitae.')

        # for tsc
        if tsc_certificate:
            try:
                if TeacherDocument.objects.filter(teacher=teacher,document_type = 'TSC Certificate').exists():
                    pass
                else:
                    TeacherDocument.objects.create(teacher = teacher,document_type = 'TSC Certificate',file = tsc_certificate)
            except:
                print('Error creating TSC Certificate .')
        else:
            messages.info(request,'Please upload TSC certificate.')


    return render(request,'settings/uploaddocuments.html',context)

@login_required(login_url='login')
def createteacherprofile(request):
    return redirect('editprofile')

def teacherfeed(request):
    teachers = Teacher.objects.all()
    context = {'teachers':teachers}
    return render(request,'teacherfeed.html',context)
















@login_required
def account_settings(request):
    context = createContext(request)
    return render(request,"settings/account.html",context)


@login_required
def privacy_settings(request):
    context = createContext(request)
    return render(request,"settings/privacy.html",context)


@login_required
def documents_settings(request):
    context = createContext(request)
    return render(request,"settings/documents.html",context)


@login_required
def notifications_settings(request):
    context = createContext(request)
    return render(request,"settings/notifications.html",context)


@login_required
def appearance_settings(request):
    context = createContext(request)
    return render(request,"settings/appearance.html",context)


@login_required
def language_settings(request):
    context = createContext(request)
    return render(request,"settings/language.html",context)


@login_required
def help_settings(request):
    context = createContext(request)
    return render(request,"settings/help.html",context)

@login_required
def changeNumber(request):
    context = createContext(request)
    if request.method == 'POST':
        new_number = request.POST.get('newnumber')
        teacher = getTeacherProfile(request)
        teacher.phone = new_number
        teacher.save()
        return redirect('/teachers/account/')


    return render(request,'settings/changenumber.html',context)

@login_required
def changePassword(request):
    context = createContext(request)
    if request.method == 'POST':
        newpassword1 = request.POST.get('newpassword1')
        newpassword2 = request.POST.get('newpassword2')

        if newpassword1 != '':
            pass
        else:
            messages.error(request,"These fields can't be blank ! ")

        if newpassword1 == newpassword2:
            # change password here
            auth.logout(request)
        else:
            messages.error(request,"Passwords don't match !")

    return render(request,'settings/changepassword.html',context)


@login_required
def changeEmail(request):
    context = createContext(request)
    teacher = getTeacherProfile(request)

    if request.method == 'POST':
        new_email = request.POST.get('newemail')
        confirm_email = request.POST.get('confirmemail')

        # Check for blank fields
        if not new_email or not confirm_email:
            messages.error(request, "Email fields can't be blank!")
            return render(request, 'settings/changeemail.html', context)

        # Check if emails match
        if new_email != confirm_email:
            messages.error(request, "Emails do not match!")
            return render(request, 'settings/changeemail.html', context)

        # Optional: check if email is different from current
        if new_email == teacher.email:
            messages.info(request, "This is already your current email!")
            return render(request, 'settings/changeemail.html', context)

        # Update email and logout user
        teacher.email = new_email
        teacher.save()
        messages.success(request, "Email updated successfully! Please log in with your new email.")
        auth.logout(request)
        return redirect('/login/')  # redirect to login page

    return render(request, 'settings/changeemail.html', context)


@login_required
def viewDocuments(request):
    context = createContext(request)
    return render(request,"settings/viewdocuments.html",context)