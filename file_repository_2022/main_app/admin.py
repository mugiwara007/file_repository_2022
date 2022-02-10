from django.contrib import admin

# Register your models here.
from .models import Profiles
from .models import UploadedFile

admin.site.register(Profiles)
admin.site.register(UploadedFile)