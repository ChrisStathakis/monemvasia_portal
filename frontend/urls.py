from django.urls import path

from .views import (HomepageView, ArticleDetailView, CategoryListView, ContactView, SearchPageView,
                    CompanyDetailView, CityListView, CityDetailView,
                    edit_company_page, link_page_view, ProductListView, ServiceListView
                    )

from .action_views import (create_new_item_view, create_new_service_view, validate_edit_form_info_view,
                           edit_delete_product_view,edit_or_delete_service_view
                           )

from catalogue.views import CategoryDetailView

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),

    path('επιχειρηση/<str:slug>/', CompanyDetailView.as_view(), name='company_view'),

    path('category/<str:slug>/', CategoryListView.as_view(), name='category'),
    path('search/', SearchPageView.as_view(), name='search'),
    path('article/<str:slug>/', ArticleDetailView.as_view(), name='article'),
    path('contact/', ContactView.as_view(), name='contact'),

    path('προϊοντα/', ProductListView.as_view(), name='product_list_view'),
    path('υπηρεσιες/', ServiceListView.as_view(), name='service_list_view'),
    path('προιοντα/κατηγοριες/', ProductListView.as_view(), name='product_categories'), # maybe will get deleted
    path('προιοντα/κατηγορια/<str:slug>/', CategoryDetailView.as_view(), name='product_category'),


    path('πολεις/', CityListView.as_view(), name='cities'),
    path('πολη/<str:slug>/', CityDetailView.as_view(), name='city_detail'),

    path('edit-view/<str:slug>/', edit_company_page, name='edit_company_page'),
    path('link/<str:slug>/', link_page_view, name='link_page'),

    # action views
    path('action/create-service/<str:slug>/', create_new_service_view, name='create_service_view'),
    path('action/create-item/<str:slug>/', create_new_item_view, name='create_item_view'),
    path('action/edit-info/<str:slug>/', validate_edit_form_info_view, name='validate_company_info'),
    path('action/edit-service/<int:pk>/<str:action>/', edit_or_delete_service_view, name='edit_or_delete_service_view'),
    path('action/edit-product/<int:pk>/<str:action>/', edit_delete_product_view, name='edit_or_delete_item_view'),

]
