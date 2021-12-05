from catalogue.models import Product
from companies.models import CompanyService, CompanyCategory, City, Company

from catalogue.categories import Category


def initial_data(request):
    print('saw it')
    return {
        'featured_products': Product.my_query.is_primary(),
        'featured_services': CompanyService.my_query.is_primary(),
        'navbar_categories': CompanyCategory.objects.filter(parent__isnull=True),
        'main_companies': Company.objects.filter(featured=True),
        'currency': 'Є',
        'cities': City.objects.filter(active=True),
        'product_categories': Category.my_query.is_parent()
    }