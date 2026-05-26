from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings

from .serializers import SignupSerializer, UserSerializer


# =========================
# COOKIE HELPER (SINGLE SOURCE)
# =========================
def set_auth_cookies(response, access_token, refresh_token):

    response.set_cookie(
        key="access_token",
        value=str(access_token),
        httponly=True,
        domain=None,
        secure=settings.COOKIE_SECURE,   # True in production (HTTPS)
        samesite=settings.COOKIE_SAMESITE,
        path="/",
        max_age=15 * 60,  # 15 minutes
    )

    response.set_cookie(
        key="refresh_token",
        value=str(refresh_token),
        httponly=True,
        domain=None,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
        max_age=7 * 24 * 60 * 60,  # 7 days
    )


# =========================
# REGISTER / SIGNUP
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):

    serializer = SignupSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response = Response(
        {
            "message": "Account created successfully",
            "user": UserSerializer(user).data,
        },
        status=status.HTTP_201_CREATED,
    )

    set_auth_cookies(response, access, refresh)

    return response


# =========================
# LOGIN
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):


    if request.content_type == "application/json":
        data=json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.data.get("username")
        password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response = Response(
        {
            "success": True,
            "user": UserSerializer(user).data,
        },
        status=status.HTTP_200_OK,
    )

    set_auth_cookies(response, access, refresh)

    return response


# =========================
# REFRESH TOKEN
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_view(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if not refresh_token:
        return Response(
            {"error": "No refresh token found"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        refresh = RefreshToken(refresh_token)
        new_access = refresh.access_token

        response = Response(
            {"refreshed": True},
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="access_token",
            value=str(new_access),
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            path=settings.COOKIE_PATH,
            max_age=15 * 60,
        )

        return response

    except Exception:
        return Response(
            {"error": "Invalid or expired refresh token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# =========================
# LOGOUT
# =========================
@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):

    response = Response(
        {"message": "Logged out successfully"},
        status=status.HTTP_200_OK,
    )

    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")

    return response


# =========================
# CURRENT USER
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):

    return Response({
        'id': request.user.id,
        'username': request.user.username
    })