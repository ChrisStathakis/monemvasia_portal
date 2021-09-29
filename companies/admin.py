from django.contrib import admin

from .models import Company, CompanyItems


class CompanyItemsInline(admin.TabularInline):
    model = CompanyItems
    fields = ['title', 'image', 'price']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ['status', 'item_support', 'priority']
    list_display = ['title', 'max_items', 'owner', 'priority', 'subscription_ends', 'status']
    readonly_fields = ['item_support', 'status', 'counter']
    search_fields = ['title', ]
    inlines = [CompanyItemsInline, ]
    fieldsets = (
        ('Active and Subs', {
            'fields': (
                ('status', 'item_support', 'max_items'),
                ('subscription_ends', 'priority', ),
            )
        }),
        ('Info', {
            'fields': (
                ('title', 'logo', 'image',),
                ('phone', 'website', 'city', 'owner', )
            )
        }),
        ('rest', {
            'fields': (
                'description',
                ('counter',)
            )
        }),


    )

