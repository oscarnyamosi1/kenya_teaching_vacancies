from rest_framework import serializers
from django.contrib.auth.models import User
from jobs.models import Job
from teachers.models import Teacher
from schools.models import School, SchoolCategory
from employers.models import Employer
from applications.models import Application
from main.models import County, Constituency, Subject, EmploymentType, Specialization, Language


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ['id', 'title']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title']


class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ['id', 'title']


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'title']


class SchoolCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolCategory
        fields = ['id', 'title']


class SchoolSerializer(serializers.ModelSerializer):
    category = SchoolCategorySerializer(read_only=True)

    class Meta:
        model = School
        fields = ['id', 'name', 'logo', 'category']


class EmployerSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Employer
        fields = ['id', 'username', 'school', 'verified']



class JobListSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer(read_only=True)
    county = CountySerializer(read_only=True)
    subjects_required = SubjectSerializer(many=True, read_only=True)
    employment_type = EmploymentTypeSerializer(read_only=True)
    days_posted = serializers.CharField(read_only=True)
    days_to_deadline = serializers.CharField(read_only=True)
    convertSalaryMin = serializers.IntegerField(read_only=True)
    convertSalaryMax = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'job_title', 'job_description', 'grade_level',
            'min_experience', 'tsc_required', 'carriculum_type',
            'salary_min', 'salary_max', 'convertSalaryMin', 'convertSalaryMax',
            'location', 'county', 'subjects_required', 'employment_type',
            'is_promoted', 'is_featured', 'is_urgent', 'is_active',
            'application_deadline', 'date_posted', 'views', 'saves',
            'total_applications', 'employer', 'days_posted', 'days_to_deadline',
        ]


class JobDetailSerializer(JobListSerializer):
    specialization_required = SpecializationSerializer(read_only=True)
    constituency = serializers.StringRelatedField()

    class Meta(JobListSerializer.Meta):
        fields = JobListSerializer.Meta.fields + ['specialization_required', 'constituency', 'applications_reviewed']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subjects_taught = SubjectSerializer(many=True, read_only=True)
    preferred_locations = CountySerializer(many=True, read_only=True)
    school_types_experienced = SchoolCategorySerializer(many=True, read_only=True)
    specializations = SpecializationSerializer(many=True, read_only=True)
    employment_type = EmploymentTypeSerializer(read_only=True)
    schools_followed = SchoolSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'phone', 'email', 'classification', 'gender',
            'date_of_birth', 'highest_education', 'institution_attended',
            'year_of_graduation', 'years_experience', 'subjects_taught',
            'grade_levels', 'school_types_experienced', 'tsc_registered',
            'tsc_number', 'specializations', 'preferred_locations',
            'willing_to_relocate', 'expected_salary_min', 'expected_salary_max',
            'employment_type', 'profile_visibility', 'verified_badge',
            'profile_picture', 'interviews_done', 'is_teacher','schools_followed'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    teacher = serializers.StringRelatedField()

    class Meta:
        model = Application
        fields = ['id', 'teacher', 'job', 'status', 'applied_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['teacher', 'employer'], write_only=True, default='teacher')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        role = validated_data.pop('role', 'teacher')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user
