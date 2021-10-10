from django.contrib import admin

from .models import Company, CompanyItems, CompanyCategory, CompanyService, CompanyInformation


class CompanyItemsInline(admin.TabularInline):
    model = CompanyItems
    fields = ['title', 'image', 'price']


class CompanyInfoInline(admin.TabularInline):
    model = CompanyInformation
    fieldsets = (
        ('images', {
            'fields': (
                ('logo_image', 'background_image', 'small_image', ),
            )
        }),
        ('Info', {
            'fields': (
                ('address', 'phone', 'cellphone', 'website', 'email'),

            )
        }),
        ('rest', {
            'fields': (
                'description',
                ('facebook_url', 'instagram_url')
            )
        }),

    )


@admin.register(CompanyCategory)
class CompanyCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    list_filter = ['parent', ]
    list_select_related = ['parent', ]


@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company']
    list_filter = ['company']





@admin.register(CompanyItems)
class CompanyItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', ]
    list_filter = ['company', ]


@admin.register(CompanyInformation)
class CompanyInformation(admin.ModelAdmin):
    list_filter = ['company']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ['status', 'business_type', 'featured', 'priority', 'category']
    list_display = ['title', 'max_items', 'owner', 'priority', 'subscription_ends', 'status']
    readonly_fields = ['item_support', 'status', 'counter']
    search_fields = ['title', ]
    inlines = [CompanyInfoInline, CompanyItemsInline, ]

    fieldsets = (
        ('Active and Subs', {
            'fields': (
                ('status',  'item_support', 'first_choice', 'featured',),
                ('business_type', 'subscription_ends', 'priority',  'max_items'),
            )
        }),
        ('Info', {
            'fields': (
                ('title', 'logo'),
                ('city', 'owner', ),
                ('category', )
            )
        }),
        ('rest', {
            'fields': (

                ('counter', 'slug')
            )
        }),


    )

