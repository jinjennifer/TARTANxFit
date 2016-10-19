from django.shortcuts import render
from .models import * 

def home(request):
    context = {}
    context['classes'] = Class.objects.all()
    return render(request, 'TxFApp/index.html', context)