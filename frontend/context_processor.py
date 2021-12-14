from django.core.cache import cache
from catalogue.models import Product
from companies.models import CompanyService, CompanyCategory, City, Company

from monemvasia_portal.cache_keys import *
from catalogue.categories import Category


def initial_data(request):
    featured_products = cache.get_or_set(FEATURED_PRODUCTS, Product.my_query.is_primary())
    featured_services = cache.get_or_set(FEATURED_SERVICES, CompanyService.my_query.is_primary())
    navbar_categories = cache.get_or_set(NAVBAR_CATEGORIES, CompanyCategory.objects.filter(parent__isnull=True))
    featured__companies = cache.get_or_set(FEATURED_COMPANIES, Company.my_query.featured())
    cities = cache.get_or_set(CITIES, City.objects.filter(active=True))
    product_categories = cache.get_or_set(PRODUCT_CATEGORIES, Category.my_query.is_parent())

    return {
        'featured_products': featured_products,
        'featured_services': featured_services,
        'navbar_categories': navbar_categories,
        'main_companies': featured__companies,
        'currency': 'Є',
        'cities': cities,
        'product_categories': product_categories
    }

