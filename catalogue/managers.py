from django.db import models


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
        qs = self.active()
        qs =

        if q:
            qs = qs.filter(title__icontains=q)


        return qs
