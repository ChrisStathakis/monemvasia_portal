from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.shortcuts import get_object_or_404

from articles.models import Article, ArticleCategory
from myAds.models import MyAd
from articles.models import Article
from companies.models import Company
import random


class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['page_title'] = 'Αρχική Σελίδα'
        featured_articles = Article.my_query.featured()
        context['featured_articles'] = featured_articles[1:]
        context['main_article'] = featured_articles.first() if featured_articles.exists() else None
        context['companies'] = Company.my_query.active()
        return context


class CategoryListView(ListView):
    model = Article
    template_name = 'list_view.html'
    paginate_by = 32

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(ArticleCategory, slug=slug)
        self.category = category
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model.objects.filter(category=self.category)
        return self.model.filter_data(self.request, qs)

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.filter(parent=self.category)
        context['category'] = self.category
        return context


class SearchPageView(ListView):
    model = Article
    template_name = 'list_view.html'
    paginate_by = 32

    def get_queryset(self):
        return self.model.filter_data(self.request, self.model.objects.all())


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'detail_view.html'
    queryset = Article.objects.all()


class ContactView(FormView):
    pass