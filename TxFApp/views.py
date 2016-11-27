from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from TxFApp.forms import *
from TxFApp.models import *
from django.contrib.auth.models import User
from django.conf import settings
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
import datetime

def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/schedule')
	elif request.method == 'GET':
		return render(request, 'TxFApp/login.html', {'form': AuthenticationForm()})
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			messages.success(request, "You have successfully logged in.")
			return HttpResponseRedirect('/schedule')
		else: 
			messages.error(request, "You have submitted incorrect credentials. Please try again.")
			return HttpResponseRedirect('/login')
		
def logout(request):
	# log the user out of the app locally and clear the session
	request.session.clear()
	auth.logout(request)
	messages.success(request, "You have successfully logged out.")
	return HttpResponseRedirect('/login')

# validate and create new user
@csrf_protect
def signup(request):
	# render sign up form
	if request.user.is_authenticated():
		return HttpResponseRedirect('/schedule')
	elif request.method == 'GET':
		reg_form = SignUpForm()
		return render(request, 'TxFApp/signup.html', {'form1': reg_form})
	# when trying to login create and save user and redirect to feed
	elif request.method == 'POST':
		reg_form = SignUpForm(data=request.POST)

		context = {}
		errors = []
		context['errors'] = errors
		
		if reg_form.is_valid():
			user = reg_form.save()

			# hash password with django default method
			user.save()

			# set role to student default in Profile subclass
			userprofile = Profile.objects.create(user=user, role='student', andrew_id=user.username)
			userprofile.save()

			# automatically log them in
			user = auth.authenticate(username=user.username, password=request.POST.get('password', ''))

			messages.success(request, "You have successfully created a new account. Please log in below to start using TARTANxFit.")
			
			if user is not None:
				auth.login(request, user)
				return render(request, 'TxFApp/schedule.html', {'form': AuthenticationForm()})
			else:
				HttpResponse('authentication failed')
				return render(request, 'TxFApp/login.html', {'form': AuthenticationForm()})
		else:
			messages.error(request, "The information you entered is not valid. Please try again.")
			return render(request, 'TxFApp/signup.html', {'form1': SignUpForm()})

	return render(request, 'TxFApp/signup.html', {'form1': reg_form})

def schedule(request, date=datetime.date.today()):
	context = {}

	user = User.objects.filter(id=request.session.get('user_id')).first()
	userprof = Profile.objects.filter(user=user).first()

	if userprof is not None:
		context['role'] = userprof.role

	classTypes = ClassType.objects.filter(start_date__lt=date,end_date__gt=date)
	if isinstance(date, datetime.date): #default date of today
		selected_date = date.strftime("%Y-%m-%d")
	else: #other dates, just taking care of how date type is processed
		selected_date = date
		date = datetime.datetime.strptime(date,"%Y-%m-%d").date()

	classes = Class.objects.filter(date=date).order_by('class_schedule__start_time')
	context['classes'] = classes
	context['userRSVPs'] = ClassAttendance.objects.filter(user=user).values_list('course', flat=True)

	#for schedule header
	dates = []
	for i in range(5):
		d = datetime.date.today() + datetime.timedelta(days=i)
		if i == 0:
			dates.append((d.strftime("%b"),d.day,d.strftime("Today"), d.strftime("%Y-%m-%d")))
		else:
			dates.append((d.strftime("%b"),d.day,d.strftime("%a"),d.strftime("%Y-%m-%d")))
	context['dates'] = dates
	context['selected_date'] = selected_date

	#rsvping for classes
	if request.method == "POST":
		user = User.objects.filter(id=request.session.get('user_id')).first()
		class_id = request.POST.get('class_id', '')
		date = request.POST.get('date','')
		try: #user has rsvped, unrsvp
			unrsvp(request, user, class_id)
			return HttpResponseRedirect('/schedule/%s/' % date)
		except: #user rvsp
			rsvp(request, user, class_id)
			return HttpResponseRedirect('/schedule/%s/' % date)

	context['active_menu_link'] = "schedule"
	return render(request, 'TxFApp/schedule.html', context)

def unrsvp(request, user, class_id):
	c = ClassAttendance.objects.filter(user=user, course=Class.objects.get(pk=class_id))[0]
	class_name = c.course.class_schedule.class_type.name
	c.delete()
	messages.success(request, "You have cancelled your RSVP for %s."% class_name)

def rsvp(request, user, class_id):
	c = ClassAttendance.objects.create(user=user, course=Class.objects.get(pk=class_id))
	c.save()
	class_name = c.course.class_schedule.class_type.name
	messages.success(request, "You have RSVP'd for %s." % class_name )

def account(request, facebook_email="xxx3maggie@aim.com", facebook_name="User User"):
	context = {}

	# create a new user in the database if one does not already exist with the facebook email
	if not User.objects.filter(email=facebook_email).exists():
		facebook_name_array = facebook_name.split()

		user = User.objects.create(username = facebook_email, first_name = facebook_name_array[0], last_name = facebook_name_array[1], email = facebook_email)
		# set the default password for all users to "test1234" so it works with authenticate
		user.set_password("test1234")
		user.save()

		# set role to student default in UserProfile subclass when creating a new account
		userprofile = Profile.objects.create(user=user, role='student')
		userprofile.save()

	if not 'user_id' in request.session:
		# Find the user in the database from Facebook login
		facebook_user = User.objects.filter(email=facebook_email).first()
		request.session['user_id'] = facebook_user.id
		context['full_name'] = facebook_user.first_name + " " + facebook_user.last_name
	else:
		facebook_user = User.objects.filter(id=request.session.get('user_id')).first()
		context['full_name'] = facebook_user.first_name + " " + facebook_user.last_name

	print(request.session.get('user_id'))

	# Log the user into the system database
	user = auth.authenticate(username=facebook_user.username, password="test1234")
	auth.login(request, user)

	userprof = Profile.objects.filter(user=facebook_user).first()

	if userprof is not None:
		context['role'] = userprof.role
		context['points'] = userprof.points

	context['rsvps'] = ClassAttendance.objects.filter(user_id=request.session.get('user_id'), course__date__gte=datetime.date.today(), attended=False).order_by("course__date", "course__class_schedule__start_time")
	context['attended'] = ClassAttendance.objects.filter(user_id=request.session.get('user_id'), course__date__lte=datetime.date.today(), attended=True).order_by("-course__date", "course__class_schedule__start_time")[:5]
	context['visits'] = len(context['attended'])
	context['competitions'] = CompetitionGroup.objects.filter(users__in=[request.session.get('user_id')])

	print(context)

	if request.method == "POST":
		user = facebook_user
		class_id = request.POST.get('class_id', '')
		form_type = request.POST.get('type', '')
		c = ClassAttendance.objects.filter(user=user, course=class_id)[0]
		if form_type == "cancel":
			unrsvp(request, user, class_id)
		elif form_type == "attended":
			c.attended = True
			c.save()
			user.profile.points += c.course.class_schedule.points
			user.profile.save()
			messages.success(request, "You attended!")
		return HttpResponseRedirect('/schedule')

	context['active_menu_link'] = "account"
	return render(request, 'TxFApp/account.html', context)

def details(request, class_id):
	context = {}

	user = User.objects.filter(id=request.session.get('user_id')).first()
	userprof = Profile.objects.filter(user=user).first()

	if userprof is not None:
		role = userprof.role
	else:
		role = request.user.profile.role
	days = dict(DAYS_OF_WEEK)
	context["role"] = role
	# Get the students attending the class if user is an admin
	if role == "admin" or role == "instructor":
		context['attendance'] = Class.objects.get(id=class_id).classattendance_set.all()

	try:
		context['class'] = Class.objects.get(pk=class_id)
		context['day'] = days.get(int(context['class'].class_schedule.day_of_week))
		try:
			context['already_rsvped'] = ClassAttendance.objects.get(user=user, course_id = class_id)
		except:
			context['already_rsvped'] = False
	except context['class'].class_schedule.DoesNotExist:
		raise Http404("GroupX Class Does Not Exist")

	if request.method == "POST":
		user = User.objects.filter(id=request.session.get('user_id')).first()
		class_id = request.POST.get('class_id', '')
		date = request.POST.get('date','')
		try: #user has rsvped, unrsvp
			unrsvp(request, user, class_id)
			return HttpResponseRedirect('/classes/%s/' % class_id)
		except: #user rvsp
			rsvp(request, user, class_id)
			return HttpResponseRedirect('/classes/%s/' % class_id)

	if Class.objects.get(id=class_id).cancelled:
		messages.error(request, "This class has been cancelled.")
	return render(request, 'TxFApp/details.html', context)

def admin(request, date=datetime.date.today()):
	context = {}

	# user = User.objects.filter(id=request.session.get('user_id')).first()
	# userprof = Profile.objects.filter(user=user).first()
	# if userprof is not None:
	# 	context['role'] = userprof.role
	# # TO DO JEN

	if request.user.is_authenticated() and request.user.profile.role == "student":
		messages.error(request, "You must be an admin to access the admin dashboard.")
		return HttpResponseRedirect('/schedule')
	classes = Class.objects.filter(date__gte=datetime.date.today()).order_by('date', '-class_schedule__start_time')
	if request.user.profile.role == "instructor":
		classes = classes.filter(class_schedule__instructor=request.user.profile.andrew_id)
	classes = classes[:15]
	context['classes'] = classes
	context['active_menu_link'] = "admin"

	# un/cancelling classesf
	if request.method == "POST":
		c = Class.objects.get(id =request.POST.get('class_id', ''))
		c.cancelled = not c.cancelled #flip to opposite cancel/uncancel
		c.save()
		class_status = "cancelled" if c.cancelled else "reinstated"
		class_name = c.class_schedule.class_type.name
		messages.success(request, "You have %s %s." % (class_status,class_name))
		return HttpResponseRedirect('/admin-dashboard')
	return render(request, 'TxFApp/admin.html', context)

def leaderboard(request):
	context = {}
	context['uid'] = request.session.get('user_id')
	context['users'] = Profile.objects.exclude(role='instructor').order_by('-points')
	return render(request, 'TxFApp/leaderboard.html', context)

def competitions(request, competition_id):
	context = {}
	context['members'] = User.objects.filter(competitiongroup__id=competition_id).order_by('-profile__points')
	context['competition'] = CompetitionGroup.objects.filter(id=competition_id).first()
	context['uid'] = request.session.get('user_id')
	return render(request, 'TxFApp/competitions.html', context)

def new_group(request):
	context = {}
	if request.method == "GET":
		form = CompetitionGroupForm()
	elif request.method == "POST":
		form = CompetitionGroupForm(request.POST)
		context['form'] = form
		if form.is_valid():
			new_group = form.save(commit=False)
			print(new_group)
			new_group.save()
			new_group.users.add(User.objects.get(id=request.session.get('user_id')))
			print(context['form'])
			messages.success(request, "Your group has been successfully created")
			return HttpResponseRedirect('/account')
	else:
		messages.error(request, "Your form input was invalid.")
	
	return render(request, 'TxFApp/new_group.html', {'form':form})