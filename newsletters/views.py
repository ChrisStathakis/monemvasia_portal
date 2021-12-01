from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect

from .models import NewsLetter
from .forms import NewsLetterFrontEndForm


def validate_newsletter_form_view(request):
    form = NewsLetterFrontEndForm(request.POST or None)
    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email', None)
        messages.success(request, f'Το Email {email} καταχωρήθηκε επιτυχώς!')
    else:
        messages.success(request, form.errors)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


