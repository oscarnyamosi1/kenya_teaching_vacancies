from django.shortcuts import render,redirect
from main.views import createContext
from django.contrib.auth.decorators import login_required
from .models import *
from myutils import *
from django.contrib import messages 
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


    return render(request,'uploaddocuments.html',context)

@login_required(login_url='login')
def createteacherprofile(request):
    return redirect('editprofile')

def teacherfeed(request):
    teachers = Teacher.objects.all()
    context = {'teachers':teachers}
    return render(request,'teacherfeed.html',context)

