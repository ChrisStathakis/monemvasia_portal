from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .models import Product, Company, Category
from .forms import ProductForm


class CategoryDetailView(ListView):
    template_name = 'product_list_view.html'
    model = Product
    paginate_by = 30

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return super(CategoryDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        childrens = self.category.children.all()
        return Product.objects.filter(active=True, category__in=childrens)

    def get_context_data(self,  **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['page_title'] = f'ΚΑΤΗΓΟΡΙΑ {self.category}'
        context['page_description'] = f'Καλώς ήρθατε στο monemvasia.org. Σε αυτή την σελίδα θα δείτε όλα τα τοπικα προϊόντα' \
                                      ' της κατηγορίας {self.category}'

        return context


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'auth_templates/form_view.html'
    form_class = ProductForm

    def get_queryset(self):
        return Product.objects.filter(company__owner=self.request.user)

    def get_success_url(self):
        return self.object.company.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = f'ΕΠΕΞΕΡΓΑΣΙΑ {self.object}'
        context['back_url'] = self.get_success_url()
        context['delete_url'] = self.object.get_delete_url()
    
        return context
    
    def form_valid(self, form):
        form.save()
        return super(ProductUpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'auth_templates/form_view.html'

    def get_queryset(self):
        return Product.objects.filter(company__owner=self.request.user)

    def get_success_url(self):
        return self.object.company.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = f'ΔΙΑΓΡΑΦΗ {self.object}'
        context['back_url'] = self.get_success_url()
        return context


