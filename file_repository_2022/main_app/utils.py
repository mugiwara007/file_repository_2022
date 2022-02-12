from distutils.command.upload import upload
from django.db.models import Q
from main_app.models import UploadedFile, Profiles


def searchQuery(request):
    search_query = ''
    if request.GET.get('search'):
        search_query = request.GET.get('search')
    return search_query


def fileSearch(request, user=''):
    search_query = searchQuery(request)

    if len(user) > 0:
        print(user)
        files = UploadedFile.objects.filter(
            (Q(file__icontains=search_query) |
             Q(file_name__icontains=search_query) |
             Q(file_type__icontains=search_query) |
             Q(uploaded_date__icontains=search_query)) &
            Q(uploader=user)
        )
        return files
    else:
        files = UploadedFile.objects.filter(
            Q(file__icontains=search_query) |
            Q(file_name__icontains=search_query) |
            Q(file_type__icontains=search_query) |
            Q(uploader__icontains=search_query) |
            Q(uploaded_date__icontains=search_query)
        )
        return files


def adminUserSearch(request):
    search_query = searchQuery(request)

    profiles = Profiles.objects.filter(username__icontains=search_query)
    return profiles
