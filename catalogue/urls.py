from django.urls import path

from .views import ProductUpdateView, ProductDeleteView, CategoryDetailView

app_name = 'catalogue'


urlpatterns = [

    path('κατηγοριες/<str:slug>/', CategoryDetailView.as_view(), name='product_category'),
    path('products/edit/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

]