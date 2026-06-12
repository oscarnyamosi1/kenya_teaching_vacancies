from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes 
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import *
from myutils import *

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCounties(request):
    return Response({"..."},status=status.HTTP_200_OK)