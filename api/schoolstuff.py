from rest_framework.response import Response
from .serializers import *
from schools.models import School
from rest_framework.decorators import api_view,permission_classes 
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from myutils import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getSchools(request):
    schools=School.objects.all()
    schoolsSerializedData=SchoolSerializer(schools,many=True)
    return Response(schoolsSerializedData.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def followSchool(request):
    schoolId = request.data["schoolId"]
    
    school = getSchool(schoolId)
    teacher = getTeacherProfile(request)
    teacher.schools_followed.add(school)
    teacher.save()

    return Response(
        {"message":"Followed School"},status=status.HTTP_200_OK
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollowSchool(request):
    schoolId = request.data["schoolId"]
    
    school = getSchool(schoolId)
    teacher = getTeacherProfile(request)
    teacherserializer = TeacherSerializer(teacher)

    teacher.schools_followed.remove(school)

    return Response(
        {"message":"unfollowed School","teacher_profile":teacherserializer.data},status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkFollow(request):
    schoolId = request.data["schoolId"]
    school = getSchool(schoolId)
    teacher = getTeacherProfile(request)
    if school in list(teacher.schools_followed.all()):
        return Response(
            {"message":"Following School","isFollowing":True},status=status.HTTP_200_OK
        )
    return Response(
        {"message":"Not following School","isFollowing":False},status=status.HTTP_200_OK
    )