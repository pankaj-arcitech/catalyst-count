from django.contrib import admin
from .models import CatalystCount, UploadedFile

# Register your models here.
admin.site.register(CatalystCount)
admin.site.register(UploadedFile)