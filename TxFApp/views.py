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

def home(request):
	context = {}
	# getting the logged in user
	context['classes'] = Class.objects.all()
	context['request_user_id'] = request.user.id
	userprof = Profile.objects.filter(user=request.user).first()
	if userprof is not None:
		context['userprof'] = userprof.role

	return render(request, 'TxFApp/index.html', context)

def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home')
	elif request.method == 'GET':
		return render(request, 'TxFApp/login.html', {'form': AuthenticationForm()})
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			messages.success(request, "You have successfully logged in.")
			return HttpResponseRedirect('/home')
		
def logout(request):
	# log the user out of the app locally
	auth.logout(request)

# validate and create new user
@csrf_protect
def signup(request):
	# render sign up form
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home')
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

			# set role to student default in UserProfile subclass
			userprofile = UserProfile.objects.create(user=user, role='student')
			userprofile.save()

			# automatically log them in
			user = auth.authenticate(username=user.username, password=request.POST.get('password', ''))

			messages.success(request, "You have successfully created a new account. Please log in below to start using TARTANxFit.")

			if user is not None:
				auth.login(request, user)
				return render(request, 'TxFApp/index.html', {'form': AuthenticationForm()})
			else:
				HttpResponse('authentication failed')
				return render(request, 'TxFApp/login.html', {'form': AuthenticationForm()})
		else:
			messages.error(request, "The information you entered is not valid. Please try again.")
			return render(request, 'TxFApp/signup.html', {'form1': SignUpForm()})

	return render(request, 'TxFApp/signup.html', {'form1': reg_form})

def schedule(request):
	context = {}
	classTypes = ClassType.objects.filter(start_date__lt=datetime.date.today(),end_date__gt=datetime.date.today())
	dow = (int(datetime.date.today().strftime("%w")) + 1) % 7
	classSchedule = ClassSchedule.objects.filter(day_of_week=dow)
	context['classes'] = classSchedule.order_by('start_time')
	dates = []
	for i in range(5):
		d = datetime.date.today() + datetime.timedelta(days=i)
		if i == 0:
			dates.append(d.strftime("%b %d Today"))
		else:
			dates.append(d.strftime("%b %d %a"))
	context['dates'] = dates
	return render(request, 'TxFApp/schedule.html', context)