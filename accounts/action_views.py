from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required


from .forms import InstagramCategoriesForm, InstagramLinkForm
from .models import InstagramCategories, InstagramLink
from companies.models import Company, CompanyService
from companies.forms import CompanyServiceForm
from catalogue.forms import ProductForm
from catalogue.models import Product


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
        return redirect(reverse('accounts:manage_links'))
    return render(request, 'auth_templates/form_view.html', context={
        'page_title': f'ΕΠΕΞΕΡΓΑΣΙΑ {instance.title}',
        'back_url': reverse('accounts:manage_links', kwargs={'slug': instance.category.company.slug}),
        'form': form,
        'delete_url': instance.get_delete_url()
    })


@login_required
def delete_category_or_link_view(request, action, pk):
    profile = request.user.profile
    instance = None
    if action == 'link':
        instance = get_object_or_404(InstagramLink, id=pk)
    if action == 'category':
        instance = get_object_or_404(InstagramCategories, id=pk)
        qs = instance.my_links.all()
        if qs.exists():
            return redirect(reverse('accounts:manage_links', kwargs={'slug': instance.company.slug}))
    if instance.profile != profile:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    instance.delete()
    return redirect(reverse('accounts:manage_links', kwargs={'slug': instance.company.slug}))


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
