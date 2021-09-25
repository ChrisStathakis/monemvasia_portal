from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.shortcuts import get_object_or_404

from articles.models import Article, ArticleCategory


class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        return context


class CategoryListView(ListView):
    model = Article
    template_name = 'list_view.html'
    paginate_by = 32

    def get_queryset(self):
        slug = self.request.kwargs['slug']
        category = get_object_or_404(ArticleCategory, slug=slug)
        qs = self.model.objects.filter(category=category)
        return self.model.filter_data(self.request, qs)


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