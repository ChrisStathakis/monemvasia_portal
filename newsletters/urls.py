from django.urls import  path
from .views import validate_newsletter_form_view


urlpatterns = [
    path('validate-newsletter/', validate_newsletter_form_view, name='validate_newsletter'),

]