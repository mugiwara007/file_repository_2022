from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('Register/', views.register, name='register'),
    path('Admin/', views.AdminHomepage, name='AdminHomepage'),
    path('User/', views.UserHomepage, name='UserHomepage'),
    path('UserProfile/', views.UserProfile, name='UserProfile'),
    path('UserChangePassword/', views.UserChangePassword, name='UserChangePassword'),
    path('UserEditAccount/', views.UserEditAccount, name='UserEditAccount'),
    path('UserArchive/', views.UserArchive, name='UserArchive'),
    path('AdminProfile/', views.AdminProfile, name='AdminProfile'),
    path('AdminEditAccount/', views.AdminEditAccount, name='AdminEditAccount'),
    path('AdminChangePassword/', views.AdminChangePassword, name='AdminChangePassword'),
    path('AdminArchive/', views.AdminArchive, name='AdminArchive'),
    path('AdminUserTab/', views.AdminUserTab, name='AdminUserTab'),
]
