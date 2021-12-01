from django.db import models
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


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
        cate_name = request.GET.getlist('category_name', None)
        city_name = request.GET.getlist('city_name', None)
        qs = self.active()
        qs = qs.filter(category__id__in=cate_name) if cate_name else qs
        qs = qs.filter(company__city__id__in=city_name) if city_name else qs

        if q:
            # vector = SearchVector('title', weight='A') + SearchVector('company__title', weight='B', config='english')
            # query = SearchQuery(q, search_type='websearch')
            # qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')
            qs = qs.filter(title__search=q)

        return qs
