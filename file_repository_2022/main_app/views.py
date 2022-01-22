from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, 'index.html')


def feed(request):
    return render(request, 'feed.html')


def about(request):
    return render(request, 'about.html')


def explore(request):
    return render(request, 'explore.html')


def contact(request):
    return render(request, 'contact.html')


def blog(request):
    return render(request, 'blog.html')
