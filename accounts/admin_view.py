from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from companies.models import Company


@method_decorator(staff_member_required, name='dispatch')
class ManageSubsView(ListView):
    template_name = 'auth_templates/manageSubsView.html'
    model = Company

    def get_queryset(self):
        return Company.objects.all()

    def get_context_data(self,  **kwargs):
        context = super(ManageSubsView, self).get_context_data(**kwargs)

        return context

