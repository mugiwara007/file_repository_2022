from django.db.models import Q
from main_app.models import UploadedFile


def search(request):
    search_query = ''
    if request.GET.get('search'):
        search_query = request.GET.get('search')
    files = UploadedFile.objects.filter(
        Q(file__icontains=search_query) |
        Q(file_name__icontains=search_query) |
        Q(file_type__icontains=search_query) |
        Q(uploader__icontains=search_query) |
        Q(uploaded_date__icontains=search_query)
    )

    return files
