from django.shortcuts import render


def term_of_use_view(request):

    return render(request, 'footer_templates/term_of_use.html')


def cookies_policy_view(request):

    return render(request, 'footer_templates/privacy.html')