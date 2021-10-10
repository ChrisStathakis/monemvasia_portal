from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView


from .models import JobPost, JobCategory


class JobPostsView(ListView):
    template_name = 'job_postings/list.html'
    model = JobPost
    paginate_by = 50

    def get_queryset(self):
        return JobPost.filter_data(self.request, JobPost.my_query.active())

    def get_context_data(self,  **kwargs):
        context = super(JobPostsView, self).get_context_data(**kwargs)
        context['job_categories'] = JobCategory.objects.all()
        return context


class JobCategoryListView(ListView):
    template_name = 'job_postings/list.html'
    model = JobPost
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        self.category = get_object_or_404(JobCategory, slug=slug)
        return super(JobCategoryListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = JobPost.my_query.filter_by_category(self.category)
        return JobPost.filter_data(self.request, qs)
