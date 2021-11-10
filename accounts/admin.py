from django.contrib import admin

from .models import Profile, InstagramCategories, InstagramLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['permission_grand', ]
    list_display = ['user', 'name', 'taxes_id', 'permission_grand']


@admin.register(InstagramCategories)
class InstagramCategoriesAdmin(admin.ModelAdmin):
    pass


@admin.register(InstagramLink)
class InstagramLinkAdmin(admin.ModelAdmin):
    pass