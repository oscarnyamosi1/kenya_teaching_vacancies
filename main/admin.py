from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Language)
admin.site.register(County)
admin.site.register(Constituency)
admin.site.register(Subject)
admin.site.register(Specialization)
admin.site.register(EmploymentType)
admin.site.register(Theme)