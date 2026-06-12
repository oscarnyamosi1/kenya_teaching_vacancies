from rest_framework.response import Response
from .serializers import TeacherSerializer
from teachers.models import Teacher
from rest_framework.decorators import api_view,permission_classes 
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from employers.models import Employer

@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def getTeacherProfile(request):
    teacherExists = Teacher.objects.filter(user=request.user).exists()
    if teacherExists:
        teacher= Teacher.objects.get(user=request.user)
        teacherSerializedData = TeacherSerializer(teacher)
    else:
        teacher='Anonymous user'
        return Response({"error":"Request Successful.No such teacher profile"},status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
        return Response(
            teacherSerializedData.data,content_type='JSON'
        )
    elif request.method == 'PATCH':
        newTeacherData = request.data
        serializer = TeacherSerializer(teacher,data=newTeacherData,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(teacherSerializedData.data|{"message":"edited"},status=status.HTTP_201_CREATED)
        return Response(teacherSerializedData.data|{"message":"Not edited.Invalid data"},status=status.HTTP_417_EXPECTATION_FAILED)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def uploaderProfile(request):
#     user = request.user
#     employerProfile = Employer.objects.get_or_create(user = user)[0]
#     employerserializer = EmployerSerializer(employerProfile)
#     return Response({"message":"employer profile"},status=status.HTTP_200_OK)