from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.conf import settings


# REGISTER

@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=400
        )

    user = User.objects.create_user(
        username=username,
        password=password
    )

    return Response({
        "message": "User created successfully"
    })


# LOGIN

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):

    username = request.data.get("username")
    password = request.data.get("password")

    userExists = User.objects.filter(email=username).exists()
    if userExists:
        newusername=User.objects.get(email = username).username
    else:
        return Response(
            {"error": "No such User"},
            status=401
        )

    user = authenticate(
        request,
        username=newusername,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=401
        )
    serializedUserData=UserSerializer(user)
    refresh = RefreshToken.for_user(user)

print(f'''



{response.cookies}



''')

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    response = Response({
        "success": True,
        "user": serializedUserData.data
    })

    # ACCESS TOKEN COOKIE

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
                path="/",
        samesite="Lax",
        max_age=60 * 15
    )

    # REFRESH TOKEN COOKIE

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
                path="/",
        samesite="Lax",
        max_age=60 * 60 * 24
    )

    return response


# REFRESH TOKEN

@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token_view(request):

    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token is None:
        return Response(
            {"error": "No refresh token"},
            status=401
        )

    try:

        refresh = RefreshToken(refresh_token)

        access_token = str(refresh.access_token)

        response = Response({
            "refreshed": True
        })

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            path="/",
            samesite="Lax",
            max_age=60 * 15
        )

        return response

    except TokenError:

        return Response(
            {"error": "Invalid refresh token"},
            status=401
        )


# LOGOUT

@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):

    response = Response({
        "message": "Logged out"
    })

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response


# PROTECTED ROUTE

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):

    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
    })
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, UserSerializer


def set_auth_cookies(response, access_token, refresh_token):

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
        max_age=15 * 60,
    )

    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=settings.COOKIE_SECURE,
        path="/",
        samesite=settings.COOKIE_SAMESITE,
        max_age=7 * 24 * 60 * 60,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):

    serializer = SignupSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    user = serializer.save()

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response = Response(
        {
            'message': 'Account created successfully',
            'user': UserSerializer(user).data,
        },
        status=status.HTTP_201_CREATED,
    )

    set_auth_cookies(response, access, refresh)

    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):

    response = Response(
        {'message': 'Logged out successfully'},
        status=status.HTTP_200_OK,
    )

    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):

    return Response(
        UserSerializer(request.user).data
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_view(request):

    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response(
            {'error': 'No refresh token found'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        refresh = RefreshToken(refresh_token)

        new_access = refresh.access_token

        response = Response(
            {'message': 'Token refreshed'},
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key='access_token',
            value=str(new_access),
            httponly=True,
            secure=settings.COOKIE_SECURE,
                    path="/",
            samesite=settings.COOKIE_SAMESITE,
            max_age=15 * 60,
        )

        return response

    except Exception:
        return Response(
            {'error': 'Invalid or expired refresh token'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

