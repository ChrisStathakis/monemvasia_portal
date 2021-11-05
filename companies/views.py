from django.shortcuts import render
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import CompanyService
from .forms import CompanyServiceForm, CompanyImageForm


@method_decorator(login_required, name='dispatch')
class CompanyServiceUpdateView(UpdateView):
    model = CompanyService
    template_name = 'auth_templates/form_view.html'
    form_class = CompanyServiceForm

    def get_queryset(self):
        return CompanyService.objects.filter(company__owner=self.request.user)

    def get_success_url(self):
        return self.object.company.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super(CompanyServiceUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = f'ΕΠΕΞΕΡΓΑΣΙΑ {self.object}'
        context['back_url'] = self.get_success_url()
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        return super(CompanyServiceUpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class CompanyServiceDeleteView(DeleteView):
    model = CompanyService
    template_name = 'auth_templates/form_view.html'

    def get_queryset(self):
        return CompanyService.objects.filter(company__owner=self.request.user)

    def get_success_url(self):
        return self.object.company.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'ΕΠΕΞΕΡΓΑΣΙΑ {self.object}'
        context['back_url'] = self.get_success_url()
        context['delete_url'] = self.object.get_delete_url()
        return context




