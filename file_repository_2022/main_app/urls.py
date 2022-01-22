from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('feed/', views.feed, name='feed'),
    path('about/', views.about, name='about'),
    path('explore/', views.explore, name='explore'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
]
