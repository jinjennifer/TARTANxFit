from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'TxFApp/index.html', context)