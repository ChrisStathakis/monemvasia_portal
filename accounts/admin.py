from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['permission_grand', ]
    list_display = ['user', 'name', 'taxes_id', 'permission_grand']