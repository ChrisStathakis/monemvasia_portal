from django.urls import path


from .views import register_view, homepage_view, login_view, dashboard_view


app_name = 'accounts'

urlpatterns = [
    path('homepage/', homepage_view, name='homepage_view'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),

    path('dashboard/', dashboard_view, name='dashboard_view')

]