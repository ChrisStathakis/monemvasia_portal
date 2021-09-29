from django.contrib import admin


from .models import MyAd
from articles.models import ArticleCategory


@admin.register(MyAd)
class MyAdManager(admin.ModelAdmin):
    list_filter = ['active', 'category']
    list_display = ['title', 'category', 'count', 'active']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['article_category'].queryset = ArticleCategory.objects.filter(parent__isnull=True)
        return super().render_change_form(request, context, *args, **kwargs)

