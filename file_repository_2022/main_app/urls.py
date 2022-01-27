from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('Admin/', views.AdminHomepage, name='AdminHomepage'),
    path('User/', views.UserHomepage, name='UserHomepage'),
]
