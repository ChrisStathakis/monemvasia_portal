from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import City, Banner


@admin.register(City)
class CityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = ['title', ]


@admin.register(Banner)
class BannerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = ['active', 'category', ]
    list_display = ['title', 'url', 'category', 'active']
