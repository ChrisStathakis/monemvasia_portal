from django.contrib import admin

# Register your models here.

from .models import BusinessContact


@admin.register(BusinessContact)
class BusinessContactAdmin(admin.ModelAdmin):
    list_filter = ['is_readed', ]
    list_display = ['email', 'name', 'afm', 'is_readed']
    search_fields = ['email', 'afm']
