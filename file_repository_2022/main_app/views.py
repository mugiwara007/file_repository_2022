from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'register.html')


def AdminHomepage(request):
    return render(request, 'AdminHomepage.html')

def UserHomepage(request):
    return render(request, 'UserHomepage.html')
    
