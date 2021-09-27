from django.shortcuts import render
from django.views.generic import ListView


from .models import JobPost


class JobPostsView(ListView):
    template_name = 'job_postings/list.html'
    model = JobPost
    paginate_by = 50

    def get_context_data(self,  **kwargs):
        context = super(JobPostsView, self).get_context_data(**kwargs)

        return context

