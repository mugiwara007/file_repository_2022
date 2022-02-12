
from multiprocessing import context
from re import search
from typing import Dict
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from main_app.models import Profiles
from main_app.models import UploadedFile

import datetime

import pytz

from django.db.models import Q
import json
from django.template.loader import render_to_string
from .utils import search
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
            return render(request, 'index.html')
# Redirect to page if user did not log out properly
    if('logged_user_type' in request.session):
        if(request.session['logged_user_type'] == True):
            return redirect('AdminHomepage')
        else:
            return redirect('UserHomepage')
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        found = Profiles.objects.filter(
            eMail=request.POST['email'], username=request.POST['userName'])
        if(not found):
            p = Profiles(username=request.POST['userName'],
                         eMail=request.POST['email'],
                         password=request.POST['password'],
                         security_question=request.POST['SQuestion'],
                         security_answer=request.POST['SAnswer'], )
            p.save()
            return render(request, 'index.html')
        else:
            # insert alert if register failed
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

        context['files'] = search(request)

        data = {'rendered_table': render_to_string(
            'table.html', context=context)}
        return JsonResponse(data)

    return render(request, 'AdminHomepage.html', context)


def UserHomepage(request):
    user = Profiles.objects.get(id=request.session['logged_id'])

    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(request.session['logged_user_type']):
        return redirect('AdminHomepage')

    context = {
        'username': user.username,
        'email': user.eMail, 'profile_picture': user.profile_picture,
        'files':  UploadedFile.objects.filter(uploader__iexact=request.session['logged_username']),
    }

    if is_ajax(request=request):

        context['files'] = search(request)

        data = {'rendered_table': render_to_string(
            'table.html', context=context)}
        return JsonResponse(data)

    return render(request, 'UserHomepage.html', context)


def UserProfile(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(request.session['logged_user_type']):
        return redirect('AdminHomepage')
    profile = Profiles.objects.get(id=request.session['logged_id'])

    context = {'username': profile.username,
               'email': profile.eMail, 'picture': profile.profile_picture}
    return render(request, 'UserProfile.html', context)


def UserChangePassword(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(request.session['logged_user_type']):
        return redirect('AdminHomepage')
    found = Profiles.objects.get(id=request.session['logged_id'])

    if request.method == 'POST':
        if request.POST['CurrentPass'] == found.password and request.POST['NewPass'] == request.POST['CNewPass']:
            found.password = request.POST['NewPass']
            found.save()
            return redirect('UserProfile')
        else:
            # insert alert
            pass
    context = {'picture': found.profile_picture}
    return render(request, 'UserChangePassword.html', context)


def UserEditAccount(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(request.session['logged_user_type']):
        return redirect('AdminHomepage')
    profile = Profiles.objects.get(id=request.session['logged_id'])

    context = {'username': profile.username,
               'email': profile.eMail, 'picture': profile.profile_picture}

    if request.method == 'POST':

        # Data validation for existing accounts
        if profile.password == request.POST['UserPassword']:
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
        # Data validation for existing accounts
        if admin.password == request.POST['UserPassword']:
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
        if request.POST['CurrentPass'] == user.password and request.POST['NewPass'] == request.POST['CNewPass']:
            user.password = request.POST['NewPass']
            user.save()
            return redirect('UserProfile')
        else:
            # insert alert
            pass

    context = {'profile_picture': user.profile_picture}
    return render(request, 'AdminChangePassword.html', context)


def AdminArchive(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')
    user = Profiles.objects.get(id=request.session['logged_id'])

    context = {'username': user.username, 'email': user.eMail,
               'profile_picture': user.profile_picture}
    return render(request, 'AdminArchive.html', context)


def AdminUserTab(request):
    if('logged_email' not in request.session):
        return render(request, 'index.html')
    if(not request.session['logged_user_type']):
        return redirect('UserHomepage')
    user = Profiles.objects.get(id=request.session['logged_id'])

    context = {'username': user.username, 'email': user.eMail,
               'profile_picture': user.profile_picture}
    return render(request, 'AdminUserTab.html', context)


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
