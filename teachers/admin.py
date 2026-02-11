from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Teacher)
admin.site.register(TeacherDocument)
admin.site.register(TeacherRating)
admin.site.register(TeacherRecommendation)