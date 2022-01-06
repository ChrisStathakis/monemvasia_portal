from django.shortcuts import render
from django.views.generic import ListView

from companies.models import Company


class ManageSubsView(ListView):
    template_name = 'auth_templates/manageSubsView.html'
    model = Company

    def get_queryset(self):
        return Company.objects.all()

    def get_context_data(self,  **kwargs):
        context = super(ManageSubsView, self).get_context_data(**kwargs)

        return context