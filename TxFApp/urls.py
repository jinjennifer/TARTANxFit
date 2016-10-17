from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from . import views
from django.views.generic import TemplateView

app_name = 'TxFApp'
urlpatterns = [
    url(r'^$', views.home, name='home'),
]

    

