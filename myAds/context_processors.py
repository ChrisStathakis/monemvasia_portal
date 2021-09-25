from .models import MyAd


def get_ads(request):
    return {
        'navbar_adds': MyAd.my_query.navbar_ads(),
    }