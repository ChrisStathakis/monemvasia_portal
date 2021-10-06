from django.urls import path

from .views import (HomepageView, ArticleDetailView, CategoryListView, ContactView, SearchPageView,
                    CompanyDetailView,
                    CityListView, CityDetailView
                    )


urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),

    path('επιχειρηση/<str:slug>/', CompanyDetailView.as_view(), name='company_view'),

    path('category/<str:slug>/', CategoryListView.as_view(), name='category'),
    path('search/', SearchPageView.as_view(), name='search'),
    path('article/<str:slug>/', ArticleDetailView.as_view(), name='article'),
    path('contact/', ContactView.as_view(), name='contact'),

    path('πολεις/', CityListView.as_view(), name='cities'),
    path('πολη/<str:slug>/', CityDetailView.as_view(), name='city_detail')
]