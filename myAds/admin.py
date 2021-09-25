from django.contrib import admin


from .models import MyAd


@admin.register(MyAd)
class MyAdManager(admin.ModelAdmin):
    list_filter = ['active', 'category']
    list_display = ['title', 'category', 'count', 'active']