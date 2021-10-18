from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


from .forms import UserCreationCustomForm, LoginForm, ProfileForm
from .models import Profile, User


def homepage_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('accounts:dashboard_view')
    return redirect('accounts:register')


@login_required
def dashboard_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    form = ProfileForm(request.POST or None, instance=profile)
    return render(request,
                  'auth_templates/dashboard.html',
                  context={
                      'user': user,
                      'form': form
                  }
                  )


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = request.POST.get('username', None)
        password = request.POST.get('password1', None)
        user = authenticate(username, password)
        login(request, user)
        return redirect('accounts:dashboard_view')

    return render(request,
                  'auth_templates/login_view.html',
                  context={
                      'form': form,
                      'page_title': 'ΣΥΝΔΕΣΗ  ΜΕΛΟΥΣ',
                      'button_title': "ΣΥΝΔΕΣΗ",
                      'button_switch_title': 'ΕΓΓΡΑΦΗ',
                      'button_switch_url': reverse('accounts:register')
})


def register_view(request):
    form = UserCreationCustomForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        afm = form.cleaned_data.get('taxes_id')
        name = form.cleaned_data.get('name')
        profile, created = Profile.objects.get_or_create(user=user)
        profile.taxes_id = afm
        profile.name = name
        profile.save()
        login(request, user)
        return redirect('accounts:dashboard_view')

    return render(request,
                  'auth_templates/login_view.html',
                  context={
                      'form': form,
                      'page_title': 'ΕΓΓΡΑΦΗ ΜΕΛΟΥΣ',
                      'button_title': "ΕΓΓΡΑΦΗ",
                      'button_switch_title': 'ΣΥΝΔΕΣΗ',
                      'button_switch_url': reverse('accounts:login')

                  })
