from django.contrib import admin
from .models import CatalystCount, UploadedFile

# Register your models here.
class CatalystCountAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'year_founded', 'industry', 'locality', 'country', 'linkedin_url', 'employees_from', 'employees_to')
admin.site.register(CatalystCount, CatalystCountAdmin)

admin.site.register(UploadedFile)