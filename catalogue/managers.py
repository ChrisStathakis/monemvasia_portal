from django.db import models
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.contrib.postgres.aggregates import StringAgg

product_search_vectors = (
    SearchVector('title', weight='A') +
    SearchVector(StringAgg('company__title', delimiter=' '), weight='B', config='english'),
    SearchVector('text', weight='D')
)

class CategoryManager(models.Manager):

    def active(self):
        return self.filter(active=True)

    def is_featured(self):
        return self.active().filter(is_featured=True)


class ProductManager(models.Manager):

    def subscribed(self):
        return self.filter(subscribe=True)

    def active(self):
        return self.subscribed().filter(active=True)

    def is_primary(self):
        return self.active().filter(is_primary=True)

    def filter_data(self, request):
        q = request.GET.get('q', None)
        cate_name = request.GET.getlist('cate_name', None)
        city_name = request.GET.getlist('city_name', None)
        qs = self.active()
        qs = qs.filter(category__slug__in=cate_name) if cate_name else qs
        qs = qs.filter(company__city__slug__in=city_name) if city_name else qs

        if q:
            # vector = SearchVector('title', weight='A') + SearchVector('company__title', weight='B', config='english')
            # query = SearchQuery(q, search_type='websearch')
            # qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')
            qs = qs.filter(title__search=q)

        return qs


    def search(self, text):
        # text = request.GET.get('q', None)
        search_query = SearchQuery(text)
        search_rank = SearchRank(product_search_vectors, search_query)
        trigram_similarity = TrigramSimilarity('title', text)
        return self.get_queryset().annotate(
            search=product_search_vectors
        ).filter(
            search=search_query
        ).annotate(
            rank=search_rank + trigram_similarity
        ).order_by('-rank')