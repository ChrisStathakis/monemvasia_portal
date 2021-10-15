from django.shortcuts import render
from django.contrib import messages
from django.views.generic import CreateView
# Create your views here.

from .models import Contact
from .forms import ContactForm


class ContactView(CreateView):
    template_name = ''
    model = Contact
    form_class = ContactForm
    success_url = ''

    def form_valid(self, form):
        messages.success(self.request, '')
        form.save()


    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)

        return context