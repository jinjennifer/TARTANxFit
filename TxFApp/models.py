from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib import admin
import datetime

ROLES = (
    ('admin', 'Administrator'), 
    ('student', 'Student'),
    ('instructor', 'Instructor')
)

DAYS_OF_WEEK = (
	('1', 'Sunday'),
    ('2', 'Monday'),
    ('3', 'Tuesday'),
    ('4', 'Wednesday'),
    ('5', 'Thursday'),
    ('6', 'Friday'),
    ('7', 'Saturday'),
)

class Profile(models.Model):
    #we are using from Django's User class, and it has the following fields:
    #username, first_name, last_name, email, password
    #is_staff, is_active, is_superuser, last_login and date_joined
    user = models.OneToOneField(User)
    andrew_id = models.CharField(max_length=100, primary_key = True)
    role = models.CharField(
        max_length = 15, 
        blank = False, 
        choices = ROLES,
        default = 'student')
    points = models.IntegerField(default=0)

    def num_points(self):
        return ClassAttendance.objects.all().filter(user=self.user,attended=True).aggregate(Sum("course__class_schedule__points")).get("course__class_schedule__points__sum")

class CompetitionGroup(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    reward = models.CharField(max_length=1000, null=True, blank=True)
    users = models.ManyToManyField(User) 

class ClassType(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    start_date = models.DateField()
    end_date = models.DateField()

class ClassSchedule(models.Model):
    day_of_week = models.CharField(max_length = 1, choices = DAYS_OF_WEEK)
    location = models.CharField(max_length = 20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    points = models. IntegerField()
    class_type = models.ForeignKey(ClassType)
    instructor = models.ForeignKey(Profile)

class ClassScheduleAdmin(admin.ModelAdmin):
    def instructor_name(self, instance):
        return instance.instructor.user.first_name + " " + instance.instructor.user.last_name

    # Change how class schedule objects are displayed in list format in the admin interface
    list_display = ('day_of_week', 'location', 'start_time', 'end_time', 'points', 'class_type', 'instructor_name')
    
class Class(models.Model):
    class Meta:
        # Change plural form
        verbose_name_plural = "Classes"

    date = models.DateField()
    cancelled = models.BooleanField(default=False)
    class_schedule = models.ForeignKey(ClassSchedule)

    def has_occurred(self):
        return (self.class_schedule.start_time <= datetime.datetime.now().time()) and (self.date <= datetime.date.today())

class ClassAttendance(models.Model):
    class Meta:
        unique_together = (('user', 'course'),)
    attended = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    course = models.ForeignKey(Class)
