from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from TxFApp import views
from django.views.static import serve
from django.conf.urls.static import static
from TxFApp.forms import ClassTypeForm, ClassScheduleForm
from TxFApp.views import ClassWizard

app_name = 'TxFApp'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^account/(?P<facebook_email>[\w.@+-]+)/$', views.account, name='account'),
    url(r'^account/(?P<facebook_email>[\w.@+-]+)/(?P<facebook_name>[\w ]+)/$', views.account, name='account'),
    url(r'^account', views.account, name='account'),
    url(r'^classes/(?P<class_id>[0-9]+)/$', views.details, name='details'),
    url(r'^schedule/(?P<date>\d{4}-\d{2}-\d{2})/$', views.schedule, name='schedule'),
    url(r'^schedule', views.schedule, name='schedule'),
    url(r'^admin-dashboard', views.admin, name='admin'),
    url(r'^leaderboard', views.leaderboard, name='leaderboard'),
    url(r'^competitions/(?P<competition_id>[0-9]+)/$', views.competitions, name='competitions'),
    url(r'^leaderboard', views.leaderboard, name='leaderboard'),
    url(r'^new-group', views.new_group, name='new_group'),
    url(r'^new-class', ClassWizard.as_view([ClassTypeForm,ClassScheduleForm]), name='new_class'),
]