from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from schools.models import SchoolCategory
from main.models import *
from employers.models import Employer
from django.contrib.auth.decorators import login_required
from django.contrib import auth

classification_choices = (
    ('Humanities','Humanities'),
    ('Sciences','Sciences'),
    ('Arts','Arts'),
    ('Math','Math')
)
class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)


    classification = models.CharField(max_length=20,choices=classification_choices,default='Arts')

    genders = (
        ('Male','Male'),
        ('Female','Female'),
        ('Rather not say','Rather not say')
    )
    gender = models.CharField(max_length=20,choices=genders,default='')
    date_of_birth = models.DateField(null=True, blank=True)

    education_levels = (
        ('Degree','Degree'),
        ('Diploma','Diploma'),
        ('Doctorate','Doctorate'),
        ('Masters','Masters')
    )
    highest_education = models.CharField(max_length=50,choices=education_levels,default='Degree')
    institution_attended = models.CharField(max_length=255)
    year_of_graduation = models.PositiveIntegerField(null=True,blank=True)

    years_experience = models.PositiveIntegerField(null=True,blank=True)
    subjects_taught = models.ManyToManyField('main.Subject',related_name='teachersubjecttaught')
    grade_levels = models.CharField(max_length=3)

    school_types_experienced = models.ManyToManyField(SchoolCategory,related_name='teacherschooltypes')
    tsc_registered = models.BooleanField(default=False)
    tsc_number = models.CharField(max_length=50, blank=True, null=True)

    teacher_subjects = models.ManyToManyField('main.Subject',related_name="teachersubjects")

    specializations = models.ManyToManyField('main.Specialization',related_name='teacherspecializations',blank=True)
    languages_spoken = models.ManyToManyField('main.Language',related_name='teacherlanguage',blank=True)

    preferred_locations = models.ManyToManyField('main.County',related_name='teacherpreferredlocation')
    willing_to_relocate = models.BooleanField(default=False)

    expected_salary_min = models.PositiveIntegerField(null=True,blank=True)
    expected_salary_max = models.PositiveIntegerField(null=True,blank=True)

    employment_type = models.ForeignKey('main.EmploymentType',on_delete=models.CASCADE,null=True,blank=True)
    profile_visibility = models.BooleanField(default=True)
    verified_badge = models.BooleanField(default=False)

    profile_picture = models.FileField(upload_to='teachers/profilepictures',null=True,blank=True)

    interviews_done = models.PositiveIntegerField(default=0)
    years_experience = models.PositiveIntegerField(default=0)

    availabe_till = models.DateTimeField(blank=True,null=True)
    has_been_hired_here = models.BooleanField(default=False)

    saved_jobs = models.ManyToManyField('jobs.Job',related_name='teacher_saved_job',blank=True)
    applied_jobs = models.ManyToManyField('jobs.Job',related_name='teacher_applied_job',blank=True)

    schools_followed = models.ManyToManyField('schools.School',related_name='teacher_followed_schools',blank=True)
    teachers_followed = models.ManyToManyField('teachers.Teacher',blank=True)

    is_teacher = models.BooleanField(default=True)
    theme = models.OneToOneField('main.Theme',on_delete=models.CASCADE,related_name='teacher_theme',null=True,blank=True)
    @property
    def teachersubjects(self):
        teachersubjectslist = self.teacher_subjects.all()
        teachersubjects = ', '.join(teachersubjectslist).capitalize()
        return f'{teachersubjects} .'

    @property
    def availability(self):
        now = timezone.now()
        if self.availabe_till is not None:
            availability_period = self.availabe_till - now
 
            if availability_period.days > 30:
                months = availability_period.days // 30
                return f"{months} months. Notice"
            elif (availability_period.days < 30) and (availability_period.days > 1):
                return f"{availability_period.days} days. Notice"
            elif availability_period.days < 1:
                return f"{availability_period.seconds//3600} hrs. Notice"
        return f"Available."


    @property
    def pref_locations(self):
        all_locations = []
        for location in self.preferred_locations.all():
            all_locations.append(location.title.capitalize())

        return f'{', '.join(all_locations)} .'

    @property
    def schoolsExperienced(self):
        school_list = []
        for school in self.school_types_experienced.all():
            school_list.append(school.title.capitalize())
        return f'{', '.join(school_list)} - '

    @property
    def min_salary(self):
        return f'{self.expected_salary_min//1000} k'
    
    @property
    def max_salary(self):
        return f'{self.expected_salary_max//1000} k'

    def __str__(self):
        return f'''Teacher {self.user.username.capitalize()}.'''
    
ratings = (
    ('0',0),
    ('1',1),
    ('2',2),
    ('3',3),
    ('4',4),
    ('5',5)
)
class TeacherRating(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    rating = models.CharField(max_length=10,choices=ratings,default=0)

document_types = (
    ('National ID','National ID'),
    ('Carriculum Vitae','Carriculum Vitae'),
    ('Degree Certificate','Degree Cerificate'),
    ('Transcript','Transcript'),
    ('Diploma Certificate','Diploma Certificate'),
    ('TSC Certificate','TSC Certificate'),
    ('Other Document','Other Document')

)


class TeacherDocument(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=10000,choices=document_types,blank=True)
    user = auth.get_user_model().username
    file = models.FileField(upload_to=f'teacher_documents/')
    
    def __str__(self):
        return f'''Documents {self.teacher}.'''
    
class TeacherRecommendation(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    comment = models.TextField(blank=True,null=True)
    recommender = models.ForeignKey(Employer,on_delete=models.CASCADE)

# from jobs.models import employment_choices