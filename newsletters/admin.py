from django.contrib import admin

from .models import NewsLetter


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ['email', 'gender', 'approve']
    list_filter = ['approve', 'gender']
