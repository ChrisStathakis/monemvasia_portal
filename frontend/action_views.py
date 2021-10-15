from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from companies.forms import CompanyItemForm, CompanyServiceForm, FrontEndCompanyInformationForm
from companies.models import Company, CompanyService, CompanyItems



@login_required
def validate_edit_form_info_view(request, slug):
    obj = get_object_or_404(Company, slug=slug)
    if not request.user == obj.owner:
        messages.warning(request, 'ΔΕ ΜΠΟΡΕΙΤΕ ΑΝ ΕΠΕΞΕΡΓΑΣΤΕΙΤΕ ΑΥΤΗ ΤΗΝ ΕΤΑΙΡΙΑ')
        return redirect(reverse('homepage'))
    instance = obj.detail
    form = FrontEndCompanyInformationForm(request.POST or None, instance=instance)
    if form.is_valid():
        messages.success(request, 'OI ΑΛΛΑΓΕΣ ΑΠΟΘΗΚΕΥΤΗΚΑΝ ΜΕ ΕΠΙΤΥΧΙΑ')
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def create_new_service_view(request, slug):
    obj = get_object_or_404(Company, slug=slug)
    if not request.user == obj.owner:
        messages.warning(request, 'ΔΕ ΜΠΟΡΕΙΤΕ ΑΝ ΕΠΕΞΕΡΓΑΣΤΕΙΤΕ ΑΥΤΗ ΤΗΝ ΕΤΑΙΡΙΑ')
        return redirect(reverse('homepage'))
    form = CompanyServiceForm(request.POST or None, initial={'company': obj})
    if form.is_valid():
        form.save()
        messages.success(request, 'ΝΕΑ ΥΠΗΡΕΣΙΑ ΠΡΟΣΤΕΘΗΚΕ')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def create_new_item_view(request, slug):
    obj = get_object_or_404(Company, slug=slug)
    count_items = obj.products.count()
    if not count_items <= obj.max_items:
        messages.success(request, f'TA ΜΕΓΙΣΤΑ ΠΡΟΪΌΝΤΑ ΠΟΥ ΜΠΟΡΕΙΤΕ ΝΑ ΕΧΕΤΕ ΕΙΝΑΙ {obj.max_items} . ΕΠΙΚΟΙΝΩΝΗΣΤΕ ΜΕ ΤΟΥΣ ΔΙΑΧΕΙΡΙΣΤΕΣ ΓΙΑ ΑΝΑΒΑΘΜΙΣΗ ΤΗΣ ΣΥΝΔΡΟΜΗ ΣΑΣ')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if not request.user == obj.owner:
        messages.warning(request, 'ΔΕ ΜΠΟΡΕΙΤΕ ΑΝ ΕΠΕΞΕΡΓΑΣΤΕΙΤΕ ΑΥΤΗ ΤΗΝ ΕΤΑΙΡΙΑ')
        return redirect(reverse('homepage'))
    form = CompanyItemForm(request.POST or None, initial={'company': obj})
    if form.is_valid():
        messages.success(request, 'ΝΕΟ ΠΡΟΪΟΝ  ΠΡΟΣΤΕΘΗΚΕ')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_or_delete_service_view(request, pk, action):
    obj = get_object_or_404(CompanyService, id=pk)
    if not request.user == obj.company.owner:
        messages.warning(request, 'ΔΕ ΜΠΟΡΕΙΤΕ ΑΝ ΕΠΕΞΕΡΓΑΣΤΕΙΤΕ ΑΥΤΗ ΤΗΝ ΕΤΑΙΡΙΑ')
        return redirect(reverse('homepage'))
    if action == 'delete':
        obj.delete()
    if action == 'edit':
        form = CompanyServiceForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Η ΥΠΗΡΕΣΙΑ {obj.title} ΕΠΕΞΕΡΓΑΣΤΗΚΕ ΕΠΙΤΥΧΩΣ')
    return render(request, '', context=locals())


@login_required
def edit_delete_product_view(request, pk, action):
    obj = get_object_or_404(CompanyItems, id=pk)
    if not request.user == obj.company.owner:
        messages.warning(request, 'ΔΕ ΜΠΟΡΕΙΤΕ ΑΝ ΕΠΕΞΕΡΓΑΣΤΕΙΤΕ ΑΥΤΗ ΤΗΝ ΕΤΑΙΡΙΑ')
        return redirect(reverse('homepage'))
    if action == 'delete':
        obj.delete()
    if action == 'edit':
        form = CompanyItemForm(request.POST or None, instance=obj)
        if form.is_valid():
            messages.success(request, f'ΤΟ ΠΡΟΪΌΝ {obj.title} ΕΠΕΞΕΡΓΑΣΤΗΚΕ ΕΠΙΤΥΧΩΣ')
            form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))