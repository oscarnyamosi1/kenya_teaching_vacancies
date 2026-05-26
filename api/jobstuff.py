from .serializers import JobListSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework import response
from rest_framework.response import Response
from jobs.models import *
from myutils import *
from rest_framework import status

from rest_framework.permissions import AllowAny,IsAuthenticated

@api_view(["GET"])
@permission_classes([AllowAny])
def getJobList(request):
    county = request.query_params.get('county')
    curriculum = request.query_params.get('curriculum')
    tsc = request.query_params.get('tsc')
    employment = request.query_params.get('employment_type')
    urgent = request.query_params.get('urgent')

    allJobs = Job.objects.all()
    jobsSerializer = JobListSerializer(allJobs,many=True)
    return Response(jobsSerializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getSavedJobs(request):
    teacher = getTeacherProfile(request)
    savedJobs = teacher.saved_jobs
    serializedJobData = JobListSerializer(savedJobs,many=True)
    return Response(serializedJobData.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMyApplications(request):
    try:
        appliedJobs = getAllJobsApplied(request)
    except:
        return Response({"No Jobs Applied" : f"Action completed with status {status.HTTP_204_NO_CONTENT}"})
    serializedAppliedJobData = JobListSerializer(appliedJobs,many=True)
    return Response(serializedAppliedJobData.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def applyJob(request,jobId:int):
    teacher = getTeacherProfile(request)
    teacherAppliedJobs = teacher.applied_jobs
    job = getJobById(jobId)

    # add job to this teachers's applied jobs

    teacherAppliedJobs.add(job)
    return Response({"status":f"job applied successfully. Action completed with status({status.HTTP_201_CREATED})"})

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteApplication(request,jobId):
    teacher = getTeacherProfile(request)
    teacherAppliedJobs = teacher.applied_jobs
    application = getJobById(jobId)
    teacherAppliedJobs.remove(application)
    return Response(
        {'messages':"deleted application successfully"},status=status.HTTP_200_OK
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def viewJob(request,savedId):
    job = getJobById(savedId)
    jobserializer = JobListSerializer(job)
    return Response(jobserializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkJobSavedStatus(request):
    jobid = request.data["jobId"]
    job = getJobById(jobid)
    teacher = getTeacherProfile(request)
    if job in teacher.saved_jobs.all():
        return Response({"isSaved":True,"message":"job is saved"},status=status.HTTP_200_OK)
    return Response({"isSaved":False,"message":"job is not saved"},status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkJobAppliedStatus(request):
    jobid = request.data["jobId"]
    job = getJobById(jobid)
    teacher = getTeacherProfile(request)
    if job in teacher.applied_jobs.all():
        return Response({"isApplied":True,"message":"job is saved"},status=status.HTTP_200_OK)
    return Response({"isApplied":False,"message":"job is not saved"},status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def saveJob(request,jobId):
    job = getJobById(jobId)
    teacher = getTeacherProfile(request)

    teacher.saved_jobs.add(job)
    saved = job in teacher.saved_jobs.all()
    return Response({"message":"job saved","saved":saved},status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unsaveJob(request,jobId):
    job = getJobById(jobId)
    teacher = getTeacherProfile(request)

    teacher.saved_jobs.remove(job)
    saved = job in teacher.saved_jobs.all()
    return Response({"message":"job saved","saved":saved},status=status.HTTP_200_OK)
