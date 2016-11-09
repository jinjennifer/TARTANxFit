from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from TxFApp import views
from django.views.static import serve
from django.conf.urls.static import static

app_name = 'TxFApp'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^account/(?P<facebook_email>\[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})/$', views.account, name='account'),
    url(r'^account', views.account, name='account'),
    url(r'^classes/(?P<class_id>[0-9]+)/$', views.details, name='details'),
    url(r'^schedule/(?P<date>\d{4}-\d{2}-\d{2})/$', views.schedule, name='schedule'),
    url(r'^schedule', views.schedule, name='schedule'),
]