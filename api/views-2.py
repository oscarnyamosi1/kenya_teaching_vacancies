from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Q, F, ExpressionWrapper, IntegerField
from django.middleware.csrf import get_token

from jobs.models import Job
from teachers.models import Teacher
from schools.models import School
from applications.models import Application
from main.models import County, Subject, EmploymentType, Specialization

from .serializers import (
    JobListSerializer, JobDetailSerializer, TeacherSerializer,
    ApplicationSerializer, RegisterSerializer, UserSerializer,
    SchoolSerializer, CountySerializer, SubjectSerializer,
    EmploymentTypeSerializer
)


# ─── AUTH ──────────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def csrf_token_view(request):
    return Response({'csrfToken': get_token(request)})


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]


    def post(self, request):
        username = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')

        if username and '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                # this excpt block is kinda unnecessary because the username is the first part of the email before the @ sign
                user_obj = User.objects.get(username=username)
                username = user_obj.username

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            teacher_data = None
            try:
                teacher = Teacher.objects.get(user=user)
                teacher_data = {'id': teacher.id, 'is_teacher': teacher.is_teacher}
            except Teacher.DoesNotExist:
                pass
            return Response({
                'user': UserSerializer(user).data,
                'teacher': teacher_data,
            })
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_with_https_cookie(request):
    token_key = request.POST.get('access_token')
    try:
        token = Token.objects.get(key=token_key)
    
        # user = token.user
        user_id = token['user_id']

        user = User.objects.get(id=user_id)
        user.backend = 'django.contrib.auth.backends.ModelBackend'

        if user:
            login(request, user)
            teacher_data = None
            try:
                teacher = Teacher.objects.get(user=user)
                teacher_data = {'id': teacher.id, 'is_teacher': teacher.is_teacher}
            except Teacher.DoesNotExist:
                pass
            return Response({
                'user': UserSerializer(user).data,
                'teacher': teacher_data
            })
    except Exception as e:
        return Response({"error":"Invalid or expired JWT token --> malik"},status=401)
    # except Token.DoesNotExist:
    #     return Response({'error': 'Invalid auth token.'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out.'})


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        role = request.data.get('role', 'teacher')
        if role == 'teacher':
            try:
                teacher = Teacher.objects.create(
                    user=user,
                    institution_attended='',
                    grade_levels='',
                )
                county = County.objects.first()
                if county:
                    teacher.preferred_locations.add(county)
            except Exception:
                pass
        login(request, user)
        return Response({'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        teacher_data = None
        try:
            teacher = Teacher.objects.get(user=request.user)
            teacher_data = {'id': teacher.id, 'is_teacher': teacher.is_teacher}
        except Teacher.DoesNotExist:
            pass
        return Response({
            'user': UserSerializer(request.user).data,
            'teacher': teacher_data,
        })


# ─── JOBS ──────────────────────────────────────────────────────────────────────

class JobListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['job_title', 'location', 'county__title', 'job_description']

    def get_queryset(self):
        qs = Job.objects.filter(is_active=True).select_related(
            'employer', 'employer__school', 'employer__school__category',
            'county', 'employment_type'
        ).prefetch_related('subjects_required')

        county = self.request.query_params.get('county')
        curriculum = self.request.query_params.get('curriculum')
        tsc = self.request.query_params.get('tsc')
        employment = self.request.query_params.get('employment_type')
        urgent = self.request.query_params.get('urgent')

        if county:
            qs = qs.filter(county__title__icontains=county)
        if curriculum:
            qs = qs.filter(carriculum_type=curriculum)
        if tsc:
            qs = qs.filter(tsc_required=True)
        if employment:
            qs = qs.filter(employment_type__title__icontains=employment)
        if urgent:
            qs = qs.filter(is_urgent=True)

        return qs.order_by('-date_posted')


class JobDetailView(generics.RetrieveAPIView):
    serializer_class = JobDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Job.objects.filter(is_active=True).select_related(
        'employer', 'employer__school', 'county', 'constituency',
        'employment_type', 'specialization_required'
    ).prefetch_related('subjects_required')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Job.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TrendingJobsView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Job.objects.filter(is_active=True).annotate(
            trend_score=ExpressionWrapper(
                F('views') + F('saves') * 3 + F('total_applications') * 5,
                output_field=IntegerField()
            )
        ).order_by('-trend_score').select_related(
            'employer', 'employer__school', 'county', 'employment_type'
        )[:10]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id, is_active=True)
        teacher = Teacher.objects.get(user=request.user)
        if job in teacher.saved_jobs.all():
            teacher.saved_jobs.remove(job)
            Job.objects.filter(pk=job.pk).update(saves=F('saves') - 1)
            return Response({'saved': False})
        else:
            teacher.saved_jobs.add(job)
            Job.objects.filter(pk=job.pk).update(saves=F('saves') + 1)
            return Response({'saved': True})
    except Job.DoesNotExist:
        return Response({'error': 'Job not found.'}, status=404)
    except Teacher.DoesNotExist:
        return Response({'error': 'Teacher profile not found.'}, status=404)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def apply_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id, is_active=True)
        teacher = Teacher.objects.get(user=request.user)
        if Application.objects.filter(teacher=teacher, job=job).exists():
            return Response({'error': 'Already applied.'}, status=400)
        Application.objects.create(teacher=teacher, job=job)
        teacher.applied_jobs.add(job)
        Job.objects.filter(pk=job.pk).update(total_applications=F('total_applications') + 1)
        return Response({'applied': True})
    except Job.DoesNotExist:
        return Response({'error': 'Job not found.'}, status=404)
    except Teacher.DoesNotExist:
        return Response({'error': 'Teacher profile not found.'}, status=404)


class SavedJobsView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        teacher = Teacher.objects.get(user=self.request.user)
        return teacher.saved_jobs.filter(is_active=True).select_related(
            'employer', 'employer__school', 'county', 'employment_type'
        )


class SavedJobIdsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
            ids = list(teacher.saved_jobs.values_list('id', flat=True))
            return Response({'saved_job_ids': ids})
        except Teacher.DoesNotExist:
            return Response({'saved_job_ids': []})


# ─── APPLICATIONS ──────────────────────────────────────────────────────────────

class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        teacher = Teacher.objects.get(user=self.request.user)
        return Application.objects.filter(teacher=teacher).select_related(
            'job', 'job__employer', 'job__employer__school', 'job__county'
        ).order_by('-applied_at')


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def withdraw_application(request, job_id):
    try:
        teacher = Teacher.objects.get(user=request.user)
        job = Job.objects.get(id=job_id)
        Application.objects.filter(teacher=teacher, job=job).delete()
        teacher.applied_jobs.remove(job)
        return Response({'withdrawn': True})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


# ─── TEACHER PROFILE ───────────────────────────────────────────────────────────

class TeacherProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        except Teacher.DoesNotExist:
            return Response({'error': 'No teacher profile found.'}, status=404)

    def patch(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
            data = request.data
            simple_fields = [
                'phone', 'email', 'classification', 'gender', 'date_of_birth',
                'highest_education', 'institution_attended', 'year_of_graduation',
                'years_experience', 'grade_levels', 'tsc_registered', 'tsc_number',
                'willing_to_relocate', 'expected_salary_min', 'expected_salary_max',
                'profile_visibility',
            ]
            for field in simple_fields:
                if field in data:
                    setattr(teacher, field, data[field])
            teacher.save()
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        except Teacher.DoesNotExist:
            return Response({'error': 'No teacher profile found.'}, status=404)


# ─── SCHOOLS ──────────────────────────────────────────────────────────────────

class SchoolListView(generics.ListAPIView):
    serializer_class = SchoolSerializer
    permission_classes = [permissions.AllowAny]
    queryset = School.objects.all().select_related('school_type')
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'location']


# ─── METADATA ─────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def metadata(request):
    counties = CountySerializer(County.objects.all(), many=True).data
    subjects = SubjectSerializer(Subject.objects.all(), many=True).data
    employment_types = EmploymentTypeSerializer(EmploymentType.objects.all(), many=True).data
    return Response({
        'counties': counties,
        'subjects': subjects,
        'employment_types': employment_types,
        'curriculum_types': ['IGCSE', '8-4-4', 'CBC/JSS', 'ECDE', 'High School'],
    })


from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from rest_framework.request import Request
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self,request:Request,*args,**kwargs) -> Response:
        response = super().post(request,*args,**kwargs)
        access_token = response.data["access"]
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=access_token,
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
        )
        return response