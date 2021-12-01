from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['title', 'company', 'active']
    list_filter = ['active', 'company']
    list_select_related = ['company', ]
    search_fields = ['title', ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_featured', 'active']
    list_filter = ['is_featured', 'active', 'parent']
    list_select_related = ['parent', ]
    search_fields = ['name', ]