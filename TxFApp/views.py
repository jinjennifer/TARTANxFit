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
	# log the user out of the app locally
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
	classTypes = ClassType.objects.filter(start_date__lt=date,end_date__gt=date)
	if type(date) == str:
		selected_date = date
		date = datetime.datetime.strptime(date,"%Y-%m-%d").date()
	else:
		selected_date = date.strftime("%Y-%m-%d")
	dow = int(date.strftime("%w")) + 1 % 7
	classSchedule = ClassSchedule.objects.filter(day_of_week=dow)
	context['classes'] = classSchedule.order_by('start_time')
	

	#for schedule header
	dates = []
	for i in range(5):
		d = datetime.date.today() + datetime.timedelta(days=i)
		if i == 0:
			dates.append((d.strftime("%b %d Today"), d.strftime("%Y-%m-%d")))
		else:
			dates.append((d.strftime("%b %d %a"),d.strftime("%Y-%m-%d")))
	context['dates'] = dates
	context['selected_date'] = selected_date
	return render(request, 'TxFApp/schedule.html', context)

def account(request):
	context = {}
	context['request_user_id'] = request.user.id
	userprof = Profile.objects.filter(user=request.user).first()
	if userprof is not None:
		context['role'] = userprof.role
		context['points'] = userprof.points
	context['rsvps'] = ClassAttendance.objects.filter(user_id=request.user.id).filter(course__date__gte=datetime.date.today())
	context['visits'] = len(ClassAttendance.objects.filter(user_id=request.user.id))
	context['competitions'] = CompetitionGroup.objects.filter(users__in=[request.user.id])
	return render(request, 'TxFApp/account.html', context)

def details(request, class_id):
	context = {}
	days = dict(DAYS_OF_WEEK)
	try:
		groupx = ClassSchedule.objects.get(pk=class_id)
		context['day'] = days.get(int(groupx.day_of_week))
	except GroupX.DoesNotExist:
		raise Http404("GroupX Class Does Not Exist")
	return render(request, 'TxFApp/details.html', {'groupx':groupx, 'context':context})