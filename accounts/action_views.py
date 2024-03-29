from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import InstagramCategoriesForm, InstagramLinkForm, LoginForm
from .models import InstagramCategories, InstagramLink
from companies.models import Company, CompanyService, CompanyImage
from companies.forms import CompanyServiceForm, CompanyImageForm
from catalogue.forms import ProductForm
from contact.forms import ContactForm, BusinessContactForm

SITE_EMAIL = settings.SITE_EMAIL


def validate_register_form_view(request):
    register_form = BusinessContactForm(request.POST or None)
    success = False
    if register_form.is_valid():
        new_user = register_form.save()
        send_mail(
            'ΑΙΤΗΣΗ ΕΓΓΡΑΦΗΣ monemvasia.org',
            'Σας ευχαριστούμε για την εγγραφή σας, θα ελέγξουμε τα στοιχεία σας και θα επικοινωνήσουμε σύντομα μαζί σας',
            SITE_EMAIL,
            [new_user.email, SITE_EMAIL],
            fail_silently=True
        )
        success = True
    else:
        print(register_form.errors)
    form = register_form
    return render(request, 'auth_templates/register_success.html', context=locals())


def validate_login_form_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard_view')
        else:
            messages.warning(request, 'Wrong credentials')
    else:
        messages.warning(request, 'We encoutered a problem. Please try again. ')
    return redirect('accounts:register')


@login_required
def validate_link_creation_view(request, slug):
    company = get_object_or_404(Company, slug=slug)
    profile = request.user.profile
    form = InstagramLinkForm(request.POST or None,
                             initial={
                                 'profile': profile,
                                 'company': company
                             }
                             )
    if form.is_valid():
        form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def validate_category_creation_view(request, slug):
    company = get_object_or_404(Company, slug=slug)
    profile = request.user.profile
    form = InstagramCategoriesForm(request.POST or None, initial={'profile': profile, 'company': company})
    if form.is_valid():
        form.save()
    else:
        print('errors', form.errors)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_category_view(request, pk):
    profile = request.user.profile
    instance = get_object_or_404(InstagramCategories, id=pk)
    if instance.profile != profile:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    form = InstagramCategoriesForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse('accounts:manage_links', kwargs={'slug': instance.company.slug}))
    return render(request, 'auth_templates/form_view.html', context={
        'page_title': f'ΕΠΕΞΕΡΓΑΣΙΑ {instance.title}',
        'back_url': reverse('accounts:manage_links', kwargs={'slug': instance.company.slug}),
        'form': form,
        'delete_url': instance.get_delete_url()
    })


@login_required
def edit_link_view(request, pk):
    profile = request.user.profile
    instance = get_object_or_404(InstagramLink, id=pk)
    if instance.profile != profile:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    form = InstagramLinkForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse('accounts:manage_links', kwargs={'slug': instance.category.company.slug}))
    return render(request, 'auth_templates/form_view.html', context={
        'page_title': f'ΕΠΕΞΕΡΓΑΣΙΑ {instance.title}',
        'back_url': reverse('accounts:manage_links', kwargs={'slug': instance.category.company.slug}),
        'form': form,
        'delete_url': instance.get_delete_url()
    })


@login_required
def delete_category_or_link_view(request, action, pk):

    if action == 'link':
        instance = get_object_or_404(InstagramLink, id=pk)
        instance.delete()

    if action == 'category':
        instance = get_object_or_404(InstagramCategories, id=pk)
        instance.my_links.all().delete()
        instance.delete()
        return redirect(reverse('accounts:manage_links', kwargs={'slug': instance.company.slug}))
    return request.META.get(HttpResponseRedirect('HTTP_REFERER'))


@login_required
def validate_company_create_product_or_service_view(request, slug, action):
    company = get_object_or_404(Company, slug=slug)
    if action == 'product':
        form = ProductForm(request.POST, request.FILES, initial={'company': company})
        if form.is_valid():
            form.save()
        else:
            print('form errors', form.errors)
    if action == 'service':
        form = CompanyServiceForm(request.POST, request.FILES, initial={'company': company})
        if form.is_valid():
            form.save()

    return redirect(company.get_edit_url())


# images views


@login_required
def validate_company_create_image_view(request, slug):
    print('here!', slug)
    company = get_object_or_404(Company, slug=slug)
    if company.owner != request.user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    form = CompanyImageForm(request.POST, request.FILES, initial={'company': company})
    images = company.images.all().count()
    if images >= company.max_items:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if form.is_valid():
        form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def update_company_image_view(request, pk):
    image = get_object_or_404(CompanyImage, id=pk)
    if image.company.owner != request.user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    form = CompanyImageForm(request.POST or None,
                            request.FILES or None,
                            instance=image
                            )
    if form.is_valid():
        form.save()
        return redirect(image.company.get_edit_url())
    else:
        print(form.errors)

    return render(request, 'auth_templates/form_view.html', context={
        'form': form,
        'page_title': f'ΕΠΕΞΕΡΓΑΣΙΑ ΕΙΚΟΝΑΣ',
        'back_url': image.company.get_edit_url(),
        'delete_url': image.get_delete_url()
    })


@login_required
def delete_company_image_view(request, pk):
    image = get_object_or_404(CompanyImage, id=pk)
    if image.company.owner != request.user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    image.delete()
    return redirect(image.company.get_edit_url())