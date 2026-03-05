from django.shortcuts import redirect,render
from teachers.models import Teacher
from schools.models import School,SchoolBlog
from django.contrib.auth.decorators import login_required
from applications.models import Application
from jobs.models import Job


def countHires():
    count = 0
    all_teachers = Teacher.objects.all()
    if all_teachers.__len__() > 0:
        for teacher in all_teachers:
            if teacher.has_been_hired_here:
                count +=1
        if count < 1000:
            return '500+'
        elif (count > 1000) and (count < 2000 ):
            return '1.8k+'
        elif (count > 2000) and (count < 3000):
            return '2.9k+'
        elif (count > 3000) and (count < 5000):
            return '5k+'
        elif (count > 5000) and (count < 10000):
            return '8k+'
        elif (count > 10000) and (count < 20000):
            return '17k+'
    return '0'


def getTrendingJobs(request):
    pass

def createContext(request):
    all_jobs = Job.objects.all().order_by('-is_featured', '-date_posted')
    teachers_hired = countHires()
    trendingjobs = getTrendingJobs(request)
    context = {"all_jobs":all_jobs,"teachers_hired":teachers_hired,'trending_jobs':trendingjobs}
    return context


def returnToPrevPage(request):
    prev_url = request.META.get('HTTP_REFERER')
    return redirect(str(prev_url))

@login_required(login_url='login')
def createMissingTeacherProfiles(request):
    user = request.user
    teacher_profiles = Teacher.objects.all()


    profile_exists = teacher_profiles.filter(user = user).exists()
    if profile_exists :
        pass
    else:
        new_teacher_profile = Teacher.objects.create(user = user,email=user.email)
        new_teacher_profile.save()
        print('teacher profile created')


@login_required(login_url='login')
def getTeacherProfile(request):
    createMissingTeacherProfiles(request) 
    if request.user.is_authenticated:
        teacher = Teacher.objects.get(user = request.user)
        return teacher
    else:
        return redirect('login')
    

@login_required(login_url='login')
def getAllJobApplications(request):
    teacher = getTeacherProfile(request)
    applications = Application.objects.filter(teacher = teacher)
    return applications

@login_required(login_url='login')
def getAllJobs(request):
    return Job.objects.all()

@login_required(login_url='login')
def getAllSchools(request):
    return School.objects.all()

@login_required(login_url='login')
def getAllSchools(request):
    return SchoolBlog.objects.all()


@login_required(login_url='login')
def getTeacherSavedJobs(request):
    teacher = getTeacherProfile(request)
    saved_jobs = teacher.saved_jobs.all()
    return saved_jobs


def countSchools():
    numberschools = len(School.objects.all())
    if numberschools > 500 and numberschools < 1000:
        return '500+'
    elif numberschools > 1000 and numberschools < 5000:
        return "3k+"
    elif numberschools > 5000 and numberschools < 10000:
        return "8k+"
    else:
        return '1.2k+'
def countActiveJobs():
    active_jobs = Job.objects.filter(is_active = True)
    return len(active_jobs)


def getJobById(id):
    job_exists = Job.objects.filter(id=id).exists()
    if job_exists:
        job = Job.objects.get(id=id)
        return job
    else:
        None

@login_required(login_url='login')
def getAllJobsApplied(request):
    teacher = getTeacherProfile(request)
    return teacher.applied_jobs.all()

def maincontext(request):
    # import school helper functions here to avoid circular imports at module load
    try:
        from schools.views import createschoolsponsor, createschoolcategory
        createschoolsponsor()
        createschoolcategory()
    except Exception:
        # If import fails (for example during migrations or when models not ready), continue
        pass

    context = createContext(request)
    context2 = {
        "number_of_schools":countSchools(),
        "active_jobs":countActiveJobs(),
        "job_applications":getAllJobApplications(request),
        "jobs_applied":getAllJobsApplied(request),
        "jobs_saved":getTeacherSavedJobs(request),
    }
    context = context|context2
    return context

def getJobApplicationById(appid):
    return Application.objects.get(id = appid)


# pagination stuff

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginateList(request,list:set,units_per_page:int):
    saved_jobs = list
    paginator = Paginator(saved_jobs, units_per_page)
    page_number = request.GET.get("page")
    try:
        saved_jobs_page = paginator.page(page_number)
    except PageNotAnInteger:
        saved_jobs_page = paginator.page(1)
    except EmptyPage:
        saved_jobs_page = paginator.page(paginator.num_pages)
    
    return saved_jobs_page


# end pagination stuff

def listToQuerySet(list,model):
    ids = [item.id for item in list]
    query_set = model.objects.filter(id__in = ids)
    return query_set

def getTeacherFollowedSchools(request):
    teacher = getTeacherProfile(request)
    teacher_followed_schools = teacher.saved_jobs.all()
    return teacher_followed_schools