from django.urls import path

app_name = 'company'

from .views import CompanyServiceUpdateView, CompanyServiceDeleteView


urlpatterns = [
    path('service-update/<int:pk>/', CompanyServiceUpdateView.as_view(), name='service_update'),
    path('service-delete/<int:pk>/', CompanyServiceDeleteView.as_view(), name='service-delete'),
]