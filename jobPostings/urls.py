from django.urls import path

app_name = 'jobPost'

from .views import JobPostsView, JobCategoryListView

urlpatterns = [
    path('list/', JobPostsView.as_view(), name='list'),
    path('κατηγορια/<str:slug>/', JobCategoryListView.as_view(), name='category_list')
]