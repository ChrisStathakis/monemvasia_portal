from django.contrib import admin

from .models import Profile, InstagramCategories, InstagramLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['permission_grand', ]
    fields = [
        'permission_grand',
        'name',
        'user',
        'taxes_id',
        'phone'

    ]
    list_display = ['user', 'name', 'phone', 'permission_grand']
    search_fields = ['user__email', 'name', 'phone']



@admin.register(InstagramCategories)
class InstagramCategoriesAdmin(admin.ModelAdmin):
    pass


@admin.register(InstagramLink)
class InstagramLinkAdmin(admin.ModelAdmin):
    pass