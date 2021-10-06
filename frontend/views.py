from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.shortcuts import get_object_or_404

from companies.models import Company, CompanyCategory, City
from jobPostings.models import JobPost


class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        context['page_title'] = 'Αρχική Σελίδα'
        context['cities'] = City.objects.filter(active=True)
        context['featured'] = Company.my_query.featured()[:6]
        context['last_five_jobs'] = JobPost.objects.all()[:5]
        context['featured_jobs'] = JobPost.my_query.featured()[:5] if JobPost.my_query.featured().exists() else None

        return context


class CategoryListView(ListView):
    model = Company
    template_name = 'list_view.html'
    paginate_by = 32

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(CompanyCategory, slug=slug)
        self.category = category
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model.objects.filter(category=self.category)
        return self.model.filter_data(self.request, qs)

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['categories'] = CompanyCategory.objects.filter(parent=self.category)
        context['category'] = self.category
        return context


class CityListView(ListView):
    template_name = 'list_view.html'
    model = City
    queryset = City.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data(**kwargs)

        return context


class CityDetailView(DetailView):
    template_name = 'detail_view.html'
    model = City
    queryset = City.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(CityDetailView, self).get_context_data(**kwargs)

        return context

class SearchPageView(ListView):
    model = Company
    template_name = 'list_view.html'
    paginate_by = 32

    def get_queryset(self):
        return self.model.filter_data(self.request, self.model.objects.all())


class ArticleDetailView(DetailView):
    model = Company
    template_name = 'detail_view.html'
    queryset = Company.objects.all()


class ContactView(FormView):
    pass