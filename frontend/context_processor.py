from catalogue.models import Product
from companies.models import CompanyService


def initial_data(request):

    return {
        'featured_products': Product.my_query.is_primary(),
        'featured_services': CompanyService.my_query.is_primary()
    }