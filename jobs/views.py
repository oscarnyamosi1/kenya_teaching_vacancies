from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from teachers.models import Teacher
from django.db.models import Q
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
from applications.models import Application
from myutils import *
import random
from schools.models import School
from main.models import County,Constituency




from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='login')
def savedjobs(request):
    context = createContext(request)
    saved_jobs = getTeacherSavedJobs(request)
    paginator = Paginator(saved_jobs, 50)
    page_number = request.GET.get('page')
    try:
        saved_jobs_page = paginator.page(page_number)
    except PageNotAnInteger:
        saved_jobs_page = paginator.page(1)
    except EmptyPage:
        saved_jobs_page = paginator.page(paginator.num_pages)
    context = context | {"saved_jobs_page": saved_jobs_page}
    return render(request, "savedjobs.html", context)


def jobfeed(request):
    context = createContext(request)
    return render(request,'jobfeed.html',context)

@login_required(login_url='login')
def postjob(request):
    return render(request,'postteachingjob.html')

@login_required(login_url='login')
def premiumurgent(request):
    return render(request,"premiumpricing.html")

@login_required(login_url='login')
def savejob(request,jobid):
    from main.views import getTeacherProfile,getJobById
    job = getJobById(jobid)
    if job is not None:
        teacher = getTeacherProfile(request)
        teacher.saved_jobs.add(job)
        teacher.save()
    else:
        messages.info(request,"Job doesn't exist !",extra_tags='warning')
    return returnToPrevPage(request)
def search(request):
    tearm = request.GET.get('jobquery') or request.GET.get('county/location')
    location_query = request.GET.get('county/location')

    if location_query is not None:
        if len(location_query) < 4:
            try:
                if tearm != '':
                    locations = County.objects.filter(
                        Q(title__icontains=tearm)
                    )
                    # jobs_frm_locations = [job for job in Job.objects.filter(county = location)]
                    jobs_frm_locations = []
                    for location in locations:
                        jobs = list(Job.objects.filter(county = location))
                        jobs_frm_locations.extend(jobs)
            
                elif location_query != '':
                    locations = County.objects.filter(
                        Q(title__icontains=tearm)
                    )
                    # jobs_frm_locations = [job for job in Job.objects.filter(county = location)]
                    jobs_frm_locations = []
                    for location in locations:
                        jobs = list(Job.objects.filter(county = location))
                        jobs_frm_locations.extend(jobs)
                    else:
                        jobs_frm_locations = []
            except:
                return HttpResponse('Location error !')
            
            try:
                if tearm != '':
                    results = Job.objects.filter(
                        Q(job_title__icontains=tearm)|
                        Q(job_description__icontains=tearm)
                        )
                    subject_results = list(Subject.objects.filter(
                        Q(title__icontains = tearm)
                    ))
                    subject_required_jobs = []
                    for subject in subject_results:
                        small_list_subjects_required_jobs = list(Job.objects.filter(subjects_required = subject))
                        print(f'''
                        




                    subject required jobs small list
                    
                    
                    
                    
                    
                    --------------->             ({small_list_subjects_required_jobs})
                                


                    
                    
                    ''')
                        subject_required_jobs.extend(small_list_subjects_required_jobs)
            
                    subject_required_jobs
                else:
                    results = []
            except:
                return  HttpResponse('Jobsearch operation error !')
            
            try:
                if tearm != '':
                    schools =list(
                            School.objects.filter(
                            Q(name__icontains=tearm)
                        )
                    )
                        # school_results.append(Job.objects.filter(employer = employer))
                    list_of_employers_for_search = []
                    for school in schools:
                        small_list_of_employers_for_search = list(Employer.objects.filter(
                            school = school
                        ))
                        list_of_employers_for_search += small_list_of_employers_for_search
                    for employer in list_of_employers_for_search:
                        jobs = list(Job.objects.filter(employer = employer))
                        schools += jobs


                else:
                    schools = []
            except:
                return HttpResponse('School search operational error !')
            

            results = list(chain(jobs_frm_locations,results,schools,subject_required_jobs))
        if len(results)<1:
            messages.info(request,'No results!')
            return returnToPrevPage(request)
    else:
        try:
            if location_query != '':
                results = []

                locations = County.objects.filter(
                    Q(title__icontains=location_query)
                )
                # jobs_frm_locations = [job for job in Job.objects.filter(county = location)]
                jobs_frm_locations = []
                for location in locations:
                    jobs = list(Job.objects.filter(county = location))
                    jobs_frm_locations.extend(jobs)
                
              
                matching_subject_results = list(Subject.objects.filter(
                    Q(title__icontains = tearm)
                ))

              
                location_query_locked_jobs = []
                for job in jobs_frm_locations:
                    if job in matching_subject_results:
                        location_query_locked_jobs.append(job)

                print(f'''
                
                location or query locked searches !
                                
                                {location_query_locked_jobs}
                                
                                
                ''')
                results += location_query_locked_jobs
            results = list(chain(results,location_query_locked_jobs))
            if len(results)<1:
                messages.info(request,'No results!')
                return returnToPrevPage(request)
        except:
            return HttpResponse('Location error !')
        


    # random.shuffle(results)
    context = createContext(request)

    context = context | {'search_results':results}
    return render(request,'searchresults.html',context)


@login_required(login_url='login')
def applyjob(request,jobid):
    job_to_apply = Job.objects.get(id=jobid)
    teacher = getTeacherProfile(request)

    # from main.views import getAllJobsApplied
    my_applications = getAllJobsApplied(request)
  
    if job_to_apply in my_applications:
        messages.info(request,'You already applied for this job !')
    else:
        teacher.applied_jobs.add(job_to_apply)
    return returnToPrevPage(request)


@login_required(login_url='login')
def withdrawsave(request,jobid):
    job = getJobById(jobid)
    teacher = getTeacherProfile(request)
    teacher.saved_jobs.remove(job)
    return returnToPrevPage(request)
def sharejob(request,jobid):
    return HttpResponse("Sharing job.")