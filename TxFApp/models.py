from django.db import models
from django.contrib.auth.models import User

# Create your models here.

ROLES = (
    ('admin', 'Administrator'), 
    ('student', 'Student'),
    ('instructor', 'Instructor')
)

DAYS_OF_WEEK = (
	(1, 'Sunday'),
    (2, 'Monday'),
    (3, 'Tuesday'),
    (4, 'Wednesday'),
    (5, 'Thursday'),
    (6, 'Friday'),
    (7, 'Saturday'),
)


class Profile(models.Model):
    #we are using from Django's User class, and it has the following fields:
    #username, first_name, last_name, email, password
    #is_staff, is_active, is_superuser, last_login and date_joined
    user = models.OneToOneField(User)
    andrew_id = models.CharField(max_length=20, primary_key = True)
    role = models.CharField(
        max_length = 15, 
        blank = False, 
        choices = ROLES,
        default = 'student')
    points = models.IntegerField(default=0)

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
    
class Class(models.Model):
    class Meta:
        # Change plural form
        verbose_name_plural = "Classes"

    date = models.DateField()
    cancelled = models.BooleanField(default=False)
    class_schedule = models.ForeignKey(ClassSchedule)

class ClassAttendance(models.Model):
    attended = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    course = models.ForeignKey(Class)
