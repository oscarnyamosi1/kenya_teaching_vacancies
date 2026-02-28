def search(request,location_q:str=''):
    context = createContext(request)
    tearm = request.GET.get('jobquery') or request.GET.get('county/location')
    location_query = request.GET.get('county/location') or location_q
    results = []
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
                    results.extend(jobs_frm_locations)
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
                        subject_required_jobs.extend(small_list_subjects_required_jobs)

                    results.extend(subject_required_jobs)
                else:
                    pass
            except:
                return  HttpResponse('Jobsearch operation error !')
            
            try:
                if tearm != '':
                    schools =list(
                            School.objects.filter(
                            Q(name__icontains=tearm)
                        )
                    )
                    list_of_employers_for_search = []
                    for school in schools:
                        small_list_of_employers_for_search = list(Employer.objects.filter(
                            school = school
                        ))
                        list_of_employers_for_search.extend(small_list_of_employers_for_search) 
                    for employer in list_of_employers_for_search:
                        jobs = list(Job.objects.filter(employer = employer))
                        schools += jobs

                


                else:
                    schools = []
                
                results.extend(list_of_employers_for_search)
                results.extend(schools)
            except:
                return HttpResponse('School search operational error !')

            # results = list(chain(jobs_frm_locations,results,schools,subject_required_jobs))
            context = context | {'search_results_page':results}

            if len(results)<1:
                messages.info(request,'No results!')
                return returnToPrevPage(request)
    else:
        try:
            if location_query != '':
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
                        
                results += location_query_locked_jobs
            # results = list(chain(results,location_query_locked_jobs))
            context = context | {'search_results_page':results}

            print(f'''
            


results positive(


                  {results}

                  )


''')
            if len(results)<1:
                messages.info(request,'No results!')
                return returnToPrevPage(request)
        except:
            return HttpResponse('Location Error')


    # random.shuffle(results)

    return render(request,'searchresults.html',context)
