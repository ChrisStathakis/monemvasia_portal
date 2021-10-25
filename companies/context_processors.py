from .models import CompanyCategory, Company, CompanyService

from catalogue.models import Product


def navbar_categories(request):
    featured_products = Product.objects.filter(active=True, is_primary=True)
    featured_services = CompanyService.objects.filter(is_primary=True)
    return {
        'categories': CompanyCategory.objects.filter(parent__isnull=True),
        'featured_products': featured_products,
        'featured_services': featured_services
    }