from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from TxFApp import views
from django.views.static import serve
from django.conf.urls.static import static

app_name = 'TxFApp'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^home', views.home, name='home'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^schedule', views.schedule, name='schedule'),
    url(r'^account', views.account, name='account')
]