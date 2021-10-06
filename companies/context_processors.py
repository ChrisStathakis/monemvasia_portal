from .models import CompanyCategory


def navbar_categories(request):

    return {
        'categories': CompanyCategory.objects.filter(parent__isnull=True)
    }