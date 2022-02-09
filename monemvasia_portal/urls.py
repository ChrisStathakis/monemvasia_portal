"""monemvasia_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),

    path('accounts/', include('accounts.urls')),
    path('αγγελιες/', include('jobPostings.urls')),
    path('catalogue/', include('catalogue.urls')),
    path('company/', include('companies.urlpatterns')),
    path('newsletter/', include('newsletters.urls')),


    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='auth_templates/reset/password_reset_form.html'),
         name='password_forgot'),
    path('reset-password-done/', auth_views.PasswordResetDoneView.as_view(template_name='auth_templates/reset/password_reset_done.html'), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-done/', auth_views.PasswordResetDoneView.as_view(), name='reset_done')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
