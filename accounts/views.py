from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login

from .forms import UserCreationCustomForm, LoginForm, ProfileForm, InstagramLinkForm, InstagramCategoriesForm
from .models import Profile, User, InstagramCategories, InstagramLink, Company
from companies.forms import FrontEndCompanyInformationForm, CompanyServiceForm
from catalogue.forms import ProductForm
from catalogue.models import Product
from contact.forms import BusinessContactForm


def homepage_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('accounts:dashboard_view')
    return redirect('accounts:register')


def logout_request(request):
    logout(request)
    return redirect('homepage')


def login_or_register_view(request):
    register_form = BusinessContactForm(request.POST or None)
    login_form = LoginForm(request.POST or None)
    page_title = 'ΠΕΡΙΟΧΗ ΜΕΛΩΝ'

    return render(request, 'auth_templates/login_view.html', context=locals())


@login_required
def dashboard_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    if not profile.permission_grand:
        return render(request, 'auth_templates/deny_access.html')
    form = ProfileForm(request.POST or None, instance=profile)
    return render(request,
                  'auth_templates/dashboard.html',
                  context={
                      'user': user,
                      'form': form
                  }
                  )


class MyLoginView(LoginView):
    template_name = 'auth_templates/login_view.html'

    def get_success_url(self):
        return reverse('accounts:dashboard_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ΣΥΝΔΕΣΗ ΜΕΛΟΥΣ'
        context['button_title'] = "ΣΥΝΔΕΣΗ"
        context['button_switch_title'] = 'ΕΓΓΡΑΦΗ'
        context['button_switch_url'] = reverse('accounts:register')
        return context


def register_view(request):
    form = UserCreationCustomForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        afm = form.cleaned_data.get('taxes_id')
        name = form.cleaned_data.get('name')
        profile, created = Profile.objects.get_or_create(user=user, taxes_id=afm, name=name)
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


@login_required
def update_profile_view(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()

        return redirect('accounts:dashboard_view')
    return render(request,
                  'auth_templates/form_view.html',
                  context={
                      'form': form,
                      'page_title': 'ΕΠΕΞΕΡΓΑΣΙΑ ΠΡΟΦΙΛ',
                      'back_url': reverse('accounts:dashboard_view')
                  })


@login_required
def update_company_info_view(request, slug):
    instance = get_object_or_404(Company, slug=slug)
    if instance.owner != request.user:
        return redirect('homepage')
    profile = instance.detail
    form = FrontEndCompanyInformationForm(request.POST or None, instance=profile, initial={'company': instance})
    if request.POST:
        form = FrontEndCompanyInformationForm(request.POST, request.FILES, instance=profile, initial={'company': instance})
        if form.is_valid():
            form.save()
            return redirect('accounts:dashboard_view')

    product_form = ProductForm(request.POST or None, initial={'company': instance})
    service_form = CompanyServiceForm(request.POST or None, initial={'company': instance})
    return render(request, 'auth_templates/company_edit_view.html', context={
        'form': form,
        'page_title': f'ΕΠΕΞΕΡΓΑΣΙΑ {instance.title}',
        'back_url': reverse('accounts:dashboard_view'),
        'company': instance,
        'product_form': product_form,
        'service_form': service_form
    })


@login_required
def manage_instagram_links_view(request, slug):
    company = get_object_or_404(Company, slug=slug)
    user = request.user
    profile = user.profile
    instagram_categories = profile.instagramcategories_set.all()
    form = InstagramLinkForm(initial={'profile': profile, 'company': company})
    category_form = InstagramCategoriesForm(initial={'profile': profile, 'company': company})
    return render(request, 'auth_templates/instagram_manager.html', context=locals())


