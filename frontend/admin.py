from django.contrib import admin


from .models import City, Banner


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_filter = ['title', ]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_filter = ['active', 'category', ]
    list_display = ['title', 'url', 'category', 'active']
