from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.core.cache import cache

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from companies.models import Company, CompanyService, City, CompanyHitCounter, ServiceHitCounter
from catalogue.forms import ProductForm
from jobPostings.models import JobPost

from companies.forms import FrontEndCompanyInformationForm, CompanyServiceForm
from companies.models import CompanyCategory
from contact.forms import ContactForm
from contact.models import Contact
from catalogue.models import Product, Category
from .models import Banner
from monemvasia_portal.cache_keys import BIG_BANNERS_KEY, MEDIUM_BANNERS_KEY


class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        context['page_title'] = 'Αρχική Σελίδα'
        context['page_description'] = 'Καλώς ήρθατε στο monemvasia.org. Εδώ θα βρείτε πληροφορίες για τις τοπικές ' \
                                      'επιχειρήσεις και προϊόντα.'

        context['big_banners'] = cache.get_or_set(BIG_BANNERS_KEY, Banner.my_query.big_banner())
        context['medium_banners'] = cache.get_or_set(MEDIUM_BANNERS_KEY, Banner.my_query.medium_banner())

        return context


class ProductListView(ListView):
    template_name = 'product_list_view.html'
    model = Product
    paginate_by = 16

    def get_queryset(self):
        self.initial_list = Product.my_query.active()
        return Product.my_query.filter_data(self.request)

    def get_context_data(self,  **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        product_cats = list(self.initial_list.values_list('category__id', flat=True).distinct())
        categories = Category.objects.filter(id__in=product_cats)
        context['prod_cat'] = categories
        context['page_title'] = 'ΠΡΟΪΟΝΤΑ'
        context['page_description'] = 'Καλώς ήρθατε στο monemvasia.org. Σε αυτή την σελίδα θα δείτε όλα τα τοπικα προϊόντα'
        context['city_filter'], context['product_cat_filter'] = 2*[True]
        return context


class ServiceListView(ListView):
    template_name = 'service_list_view.html'
    model = CompanyService
    paginate_by = 30

    def get_queryset(self):
        return CompanyService.my_query.filter_data(self.request)

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['prod_cat'] = Category.objects.filter(active=True, parent__isnull=True)
        context['page_title'] = 'ΥΠΗΡΕΣΙΕΣ'
        context['page_description'] = 'Καλώς ήρθατε στο monemvasia.org. Σε αυτή την σελίδα θα δείτε όλα τις υπηρεσίες της περιοχής'
        context['city_filter'] = True
        return context


class CompanyDetailView(DetailView):
    model = Company
    queryset = Company.my_query.active()
    template_name = 'company_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        CompanyHitCounter.update_hit(self.request, self.object)
        context['profile'] = self.object.detail
        context['back_url'] = HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        context['page_title'] = f'{self.object}'
        context['products'] = Product.my_query.active().filter(company=self.object)
        context['services'] = CompanyService.my_query.active().filter(company=self.object)
        context['photos'] = self.object.images.filter(background_img=False)
        return context


class CategoryParentListView(ListView):
    model = CompanyCategory
    template_name = 'company_category_list_view.html'
    paginate_by = 32

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(CompanyCategory, slug=slug)
        self.category = category
        self.slug = slug
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return CompanyCategory.objects.filter(parent=self.category)

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ΚΑΤΗΓΟΡΙΕΣ'

        return context


class CategoryListView(ListView):
    model = Company
    template_name = 'company_list_view.html'
    paginate_by = 32

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(CompanyCategory, slug=slug)
        self.category = category
        self.slug = slug
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        return Company.my_query.filter_data(self.request, slug=self.slug)

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['my_categories'] = CompanyCategory.objects.filter(parent=self.category)
        context['cities'] = City.objects.filter(active=True)
        context['category'] = self.category
        context['page_title'] = f'{self.category}'
        context['page_description'] = f'Καλώς ήρθατε στο monemvasia.org. Επισκευτείτε την κατηγορια {self.category} ' \
                                      f'και δείτε τις τοπικές επιχειρήσεις'
        context['city_filter'] = True
        context['company_category_filter'] = True
        return context


class CityListView(ListView):
    template_name = 'city_list_view.html'
    model = City
    queryset = City.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data(**kwargs)
        context['page_title'] = 'ΠΕΡΙΟΧΕΣ'
        return context


class CityDetailView(ListView):
    template_name = 'city_detail_view.html'
    model = Company
    paginate_by = 16

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        self.city = get_object_or_404(City, slug=slug)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.filter_data(self.request, Company.my_query.active().filter(city=self.city))

    def get_context_data(self, **kwargs):
        context = super(CityDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.city
        context['company_category_filter'] = True
        context['city'] = self.city
        context['my_categories'] = CompanyCategory.objects.filter(parent__isnull=True)

        return context


class SearchPageView(TemplateView):
    template_name = 'search_page.html'

    def get_context_data(self, **kwargs):
        context = super(SearchPageView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        context['products'] = Product.my_query.filter_data(self.request)[:30]
        context['companies'] = Company.my_query.filter_data(self.request)
        context['services'] = CompanyService.my_query.filter_data(self.request)
        context['page_title'] = f'ΑΝΑΖΗΤΗΣΗ {q}'
        return context


class ArticleDetailView(DetailView):
    model = Company
    template_name = ''
    queryset = Company.objects.all()


class ContactView(CreateView):
    template_name = 'contact_page.html'
    form_class = ContactForm
    model = Contact
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['page_title'] = 'ΕΠΙΚΟΙΝΩΝΙΑ'
        return context

    def form_valid(self, form):
        form.save()

        return super(ContactView, self).form_valid(form)


def link_page_view(request, slug):
    company = get_object_or_404(Company, slug=slug)
    link_categories = company.instagramcategories_set.all()

    return render(request, 'link_page.html', context={
        'company': company,
        'link_categories': link_categories
    })