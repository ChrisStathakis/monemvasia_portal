from django.urls import path

app_name = 'jobPost'

from .views import JobPostsView

urlpatterns = [
    path('list/', JobPostsView.as_view(), name='list'),
]