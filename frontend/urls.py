from django.urls import path

from .views import (HomepageView, ArticleDetailView, CategoryListView, ContactView, SearchPageView)


urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('category/<str:slug>/', CategoryListView.as_view(), name='category'),
    path('search/', SearchPageView.as_view(), name='search'),
    path('article/<str:slug>/', ArticleDetailView.as_view(), name='article'),
    path('contact/', ContactView.as_view(), name='contact')
]