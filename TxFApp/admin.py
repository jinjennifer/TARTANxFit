from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from TxFApp.models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True

class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

admin.site.register(Profile)
admin.site.register(CompetitionGroup)
admin.site.register(ClassType)
admin.site.register(ClassSchedule, ClassScheduleAdmin)
admin.site.register(Class)
admin.site.register(ClassAttendance)