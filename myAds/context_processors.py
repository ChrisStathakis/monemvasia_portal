from .models import MyAd

import random


def get_ads(request):

    navbar_ads_qs = MyAd.my_query.navbar_ads()
    main_ads_qs = MyAd.my_query.main_adds()
    page_ads_qs = MyAd.my_query.page_ads()

    navbar_ads_choice = random.choice(list(navbar_ads_qs)) if navbar_ads_qs.exists() else None
    main_ads_choice = random.sample(list(main_ads_qs), 5) if main_ads_qs.exists() else None
    page_ads_choice = random.sample(list(page_ads_qs), 10) if page_ads_qs.exists() else None

    return {
        'navbar_adds': MyAd.my_query.navbar_ads(),

        'navbar_ads_choice': navbar_ads_choice,
        'main_ads_choice': main_ads_choice,
        'page_ads_choice': page_ads_choice

    }