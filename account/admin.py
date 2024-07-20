from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import CatalystCount

# Register your models here.
@admin.register(CatalystCount)
class CatalystCountAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'domain', 'industry', 'year_founded', 'employees_from', 'employees_to')