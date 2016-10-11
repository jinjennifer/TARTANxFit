from django.db import models
from django.contrib.auth.models import User

# Create your models here.

ROLES = (
    ('admin', 'Administrator'), 
    ('student', 'Student'),
    ('prof', 'Professor'),
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
    andrew_id = models.CharField(max_length=20)
    role = models.CharField(
        max_length = 15, 
        blank = False, 
        choices = ROLES,
        default = 'student')
    #do we want to update points/make edit record every time? 
    points = models.IntegerField()

    def numpoints(self):
    	return 

class GroupX(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)

class GroupXClass(models.Model):
    group = models.ForeignKey(GroupX)
    instructor = models.ForeignKey(User)
    day = models.CharField(max_length = 1, choices = DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    studio = models.CharField(max_length = 20)
    active = models.BooleanField(default=True)


    def points(self): #function of length of class
    	return 

class GroupXAttendance(models.Model):
	user = models.ForeignKey(User)
	group = models.ForeignKey(GroupXClass)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True)



