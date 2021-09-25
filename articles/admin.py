from django.contrib import admin

# Register your models here.
from .models import ArticleCategory, Article, ArticlePhotos


class PhotosInline(admin.TabularInline):
    model = ArticlePhotos


class CategoryInline(admin.TabularInline):
    model = ArticleCategory
    readonly_fields = ['have_children']
    fields = ['have_children', 'title', 'parent', 'slug']


@admin.register(ArticleCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'have_children']
    readonly_fields = ['have_children']
    list_filter = ['have_children', 'parent']
    fields = ['have_children', 'title', 'parent', 'slug']
    inlines = [CategoryInline, ]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'publish']
    list_filter = ['publish', 'category', 'city']
    inlines = [PhotosInline, ]
