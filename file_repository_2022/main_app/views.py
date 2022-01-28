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

def UserProfile(request):
    return render(request, 'UserProfile.html')

def UserChangePassword(request):
    return render(request, 'UserChangePassword.html')

def UserEditAccount(request):
    return render(request, 'UserEditAccount.html')

def UserArchive(request):
    return render(request, 'UserArchive.html')

def AdminProfile(request):
    return render(request, 'AdminProfile.html')

def AdminEditAccount(request):
    return render(request, 'AdminEditAccount.html')

def AdminChangePassword(request):
    return render(request, 'AdminChangePassword.html')
    
