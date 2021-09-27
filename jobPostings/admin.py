from django.contrib import admin

from .models import JobCategory, JobPost


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'publish']
    list_filter = ['publish', 'category', 'company']
    search_fields = ['title']
    list_select_related = ['category', 'company']
