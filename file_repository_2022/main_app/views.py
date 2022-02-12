
from contextlib import redirect_stderr
from multiprocessing import context
from re import search
from typing import Dict
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from main_app.models import Profiles
from main_app.models import UploadedFile
from main_app.models import Archive


import datetime

import pytz

from django.db.models import Q
import json
from django.template.loader import render_to_string
from .utils import fileSearch, adminUserSearch
# Create your views here.


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def index(request):
    # Login
    if request.method == 'POST':

        # Clear Log out session
        if('Logged-out' in request.POST):
            del request.session['logged_username']
            del request.session['logged_email']
            del request.session['logged_id']
            del request.session['logged_user_type']
            return redirect('index')
        try:
            if "@" in request.POST['user-email']:
                found = Profiles.objects.get(
                    eMail=request.POST['user-email'], password=request.POST['pwd'])
            else:
                found = Profiles.objects.get(
                    username=request.POST['user-email'], password=request.POST['pwd'])
            request.session['logged_username'] = found.username
            request.session['logged_email'] = found.eMail
            request.session['logged_id'] = found.id
            if(found.admin and request.POST['user-type'] == "Admin"):
                request.session['logged_user_type'] = found.admin
                return redirect('AdminHomepage')
            elif(not found.admin and request.POST['user-type'] == "User"):
                request.session['logged_user_type'] = found.admin
                return redirect('UserHomepage')
        except:
            messages.error(request, "Invalid Username or Password")
            return redirect('index')
# Redirect to page if user did not log out properly
    if('logged_user_type' in request.session):
        if(request.session['logged_user_type'] == True):
            return redirect('AdminHomepage')
        else:
            return redirect('UserHomepage')
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        try:
            registerError=0
            if(Profiles.objects.filter(eMail=request.POST['email'])):
                messages.error(request, "Email already exist")
                registerError+=1
            if(Profiles.objects.filter(username=request.POST['userName'])):
                messages.error(request, "Username already exist")
                registerError+=1
            if(request.POST['password'] != request.POST['c-password']):
                messages.error(request, "Password does not match")
                registerError+=1
            if(registerError != 0):
                return redirect('register')
            else:
                p = Profiles(username=request.POST['userName'],
                         eMail=request.POST['email'],
                         password=request.POST['password'],
                         security_question=request.POST['SQuestion'],
                         security_answer=request.POST['SAnswer'], )
                p.save()
                return render(request, 'index.html')
        except:
            pass
    return render(request, 'register.html')


def AdminHomepage(request):
    user = Profiles.objects.get(id=request.session['logged_id'])

    # URL ACCESS REDIRECT
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')

    files = UploadedFile.objects.all()
    context = {'username': user.username, 'email': user.eMail,
               'profile_picture': user.profile_picture,
               'files': files}

    if is_ajax(request=request):

        context['files'] = fileSearch(request)

        data = {'rendered_table': render_to_string(
            'table_files.html', context=context)}
        return JsonResponse(data)

    return render(request, 'AdminHomepage.html', context)


def UserHomepage(request):
    user = Profiles.objects.get(id=request.session['logged_id'])

    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(request.session['logged_user_type']):
        return redirect('AdminHomepage')
    # files = UploadedFile.objects.all()
    context = {
        'username': user.username,
        'email': user.eMail, 'profile_picture': user.profile_picture,
        'files':  UploadedFile.objects.filter(uploader__iexact=request.session['logged_username']),
    }

    if is_ajax(request=request):

        context['files'] = fileSearch(
            request, request.session['logged_username'])

        data = {'rendered_table': render_to_string(
            'table_files.html', context=context)}
        return JsonResponse(data)

    return render(request, 'UserHomepage.html', context)


def UserProfile(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(request.session['logged_user_type']):
        return redirect('AdminHomepage')
    profile = Profiles.objects.get(id=request.session['logged_id'])
    context = {'username': profile.username,
               'email': profile.eMail, 
               'picture': profile.profile_picture,
               }
    return render(request, 'UserProfile.html', context)


def UserChangePassword(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(request.session['logged_user_type']):
        return redirect('AdminHomepage')
    found = Profiles.objects.get(id=request.session['logged_id'])

    if request.method == 'POST':
        errorCount=0
        if(found.password != request.POST['CurrentPass']):
            messages.error(request,"Wrong Current Password")
            errorCount+=1
        if(request.POST['NewPass'] != request.POST['CNewPass']):
            messages.error(request,"Password confirmation did not match")
            errorCount+=1
        if(errorCount==0):
            found.password = request.POST['NewPass']
            found.save()
            return redirect('UserProfile')
        else:
            return redirect('UserChangePassword')
        
    context = {'picture': found.profile_picture}
    return render(request, 'UserChangePassword.html', context)


def UserEditAccount(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(request.session['logged_user_type']):
        return redirect('AdminHomepage')
    profile = Profiles.objects.get(id=request.session['logged_id'])


    if request.method == 'POST':
        errorCount = 0
        if(Profiles.objects.filter(username=request.POST['NewUserUsername']) and profile.username != request.POST['NewUserUsername']):
            messages.error(request,"New Username already taken")
            errorCount+=1
        if(Profiles.objects.filter(eMail=request.POST['NewUserEmail']) and profile.eMail != request.POST['NewUserEmail']):
            messages.error(request,"New email already been used")
            errorCount+=1
        if(profile.password != request.POST['UserPassword']):
            messages.error(request,"Wrong Password")
            errorCount+=1

        # Data validation for existing accounts
        if(errorCount==0):
            profile.username = request.POST['NewUserUsername']
            profile.eMail = request.POST['NewUserEmail']
            profile.save()
            try:
                if(not request.FILES['UserPFP'] == ''):
                    profile.profile_picture = request.FILES['UserPFP']
                    profile.save()
            except:
                pass
            return redirect('UserProfile')
        
        return redirect('UserEditAccount')
    context = {'username': profile.username,
               'email': profile.eMail, 'picture': profile.profile_picture}
    return render(request, 'UserEditAccount.html', context)


def UserArchive(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(request.session['logged_user_type']):
        return redirect('AdminHomepage')
    user = Profiles.objects.get(id=request.session['logged_id'])

    context = {'username': user.username, 'email': user.eMail,
               'profile_picture': user.profile_picture}
    return render(request, 'UserArchive.html', context)


def AdminProfile(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')
    user = Profiles.objects.get(id=request.session['logged_id'])

    context = {'username': user.username, 'email': user.eMail,
               'profile_picture': user.profile_picture}
    return render(request, 'AdminProfile.html', context)


def AdminEditAccount(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')
    admin = Profiles.objects.get(id=request.session['logged_id'])

    if request.method == 'POST':
        errorCount = 0
        if(Profiles.objects.filter(username=request.POST['NewUserUsername']) and admin.username != request.POST['NewUserUsername']):
            messages.error(request,"New Username already taken")
            errorCount+=1
        if(Profiles.objects.filter(eMail=request.POST['NewUserEmail']) and admin.eMail != request.POST['NewUserEmail']):
            messages.error(request,"New email already been used")
            errorCount+=1
        if(admin.password != request.POST['UserPassword']):
            messages.error(request,"Wrong Password")
            errorCount+=1

        # Data validation for existing accounts
        if(errorCount==0):
            admin.username = request.POST['NewUserUsername']
            admin.eMail = request.POST['NewUserEmail']
            admin.save()
            try:
                if(not request.FILES['AdminPFP'] == ''):
                    admin.profile_picture = request.FILES['AdminPFP']
                    admin.save()
            except:
                pass
            return redirect('AdminProfile')
        else:
            return redirect('AdminEditAccount')
    context = {'username': admin.username, 'email': admin.eMail,
               'profile_picture': admin.profile_picture}
    return render(request, 'AdminEditAccount.html', context)


def AdminChangePassword(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')
    user = Profiles.objects.get(id=request.session['logged_id'])
    if request.method == 'POST':
        errorCount=0
        if(user.password != request.POST['CurrentPass']):
            messages.error(request,"Wrong Current Password")
            errorCount+=1
        if(request.POST['NewPass'] != request.POST['CNewPass']):
            messages.error(request,"Password confirmation did not match")
            errorCount+=1


        if(errorCount==0):
            user.password = request.POST['NewPass']
            user.save()
            return redirect('AdminProfile')
        else:
            return redirect('AdminChangePassword')

    context = {'profile_picture': user.profile_picture}
    return render(request, 'AdminChangePassword.html', context)


def AdminArchive(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')
    user = Profiles.objects.get(id=request.session['logged_id'])

    archives = Archive.objects.all()
    context = {
        'username': user.username, 
        'email': user.eMail,
        'profile_picture': user.profile_picture,
        'archive_list':archives}
    return render(request, 'AdminArchive.html', context)


def AdminUserTab(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')
    user = Profiles.objects.get(id=request.session['logged_id'])

    profiles = Profiles.objects.all()

    context = {'username': user.username, 'email': user.eMail,
               'profile_picture': user.profile_picture,
               'profiles': profiles}

    if is_ajax(request=request):

        context['profiles'] = adminUserSearch(request)

        data = {'rendered_table': render_to_string(
            'table_adminUser.html', context=context)}
        return JsonResponse(data)

    return render(request, 'AdminUserTab.html', context,)


def AdminFileArchive(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')
    user = Profiles.objects.get(id=request.session['logged_id'])

    context = {'username': user.username, 'email': user.eMail,
               'profile_picture': user.profile_picture}
    return render(request, 'AdminFileArchive.html', context)


def AdminCreateUser(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')
    return render(request, 'AdminCreateUser.html')


def AdminEditUser(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')
    return render(request, 'AdminEditUser.html')


def uploadFile(request):
    if request.method == 'POST':
        tz = pytz.timezone('Asia/Hong_Kong')
        now = datetime.datetime.now(tz)
        upload = UploadedFile(file=request.FILES['file'],
                              file_name=request.POST.get('file_name'),
                              file_type=request.POST.get('file_type'),
                              uploader=request.session['logged_username'],
                              uploaded_date=str(now))

        upload.save()

        return redirect('UserHomepage')

def delete_user(request):
    user_id = request.GET.get('user_id')
    profile = Profiles.objects.get(id=int(user_id))
    archive = Archive(
                 username=profile.username,
                 eMail=profile.eMail,
                 password=profile.password,
                 security_question=profile.security_question,
                 security_answer=profile.security_answer,
                 user_id=profile.id)
    archive.save()
    Profiles.objects.filter(id=user_id).update(archived=True)
    return redirect(request.META['HTTP_REFERER'])

def retrieve_user(request):
    user_id = request.GET.get('user_id')
    Archive.objects.filter(user_id=int(user_id)).delete()
    Profiles.objects.filter(id=user_id).update(archived=False)
    return redirect(request.META['HTTP_REFERER'])

def permanent_delete_user(request):
    user_id = request.GET.get('user_id')
    Archive.objects.filter(user_id=int(user_id)).delete()
    Profiles.objects.filter(id=user_id).delete()
    return redirect(request.META['HTTP_REFERER'])
# hello world
