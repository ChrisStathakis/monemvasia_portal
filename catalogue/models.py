from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

import datetime
from tinymce.models import HTMLField
from .categories import Category
from companies.models import Company
from .managers import ProductManager


def upload_to(instance, filename):
    return f'/products/{instance.title}/{filename}'


class Product(models.Model):
    subscribe = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False, )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='my_products')
    title = models.CharField(max_length=220)
    image = models.ImageField(blank=True, upload_to='company/images/', )
    is_offer = models.BooleanField(default=False, verbose_name='Προσφορά')
    category = models.ManyToManyField(Category, blank=True, verbose_name='Κατηγορία')
    notes = models.TextField(null=True, blank=True, verbose_name='Περιγραφή')

    #  site
    sku = models.CharField(max_length=150, blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True, max_length=240, db_index=True)
    product_url = models.URLField(blank=True, null=True)

    # price sell and discount sells
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, verbose_name="Αρχική Τιμή")
    price_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Εκπτωτική Τιμή')
    final_price = models.DecimalField(default=0, decimal_places=2, max_digits=10, blank=True, verbose_name='Τιμή Πώλησης')

    vector_column = SearchVectorField(null=True, blank=True)
    counter = models.IntegerField(default=0)

    objects = models.Manager()
    my_query = ProductManager()

    class Meta:
        indexes = (GinIndex(fields=["vector_column"]), )
        verbose_name_plural = 'ΠΡΟΪΟΝΤΑ'

    def save(self, *args, **kwargs):
        self.subscribe = self.company.status
        if not self.product_url:
            self.product_url = self.company.detail.website
        self.final_price = self.price_discount if self.price_discount > 0 else self.price
        self.counter = self.hits.count()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.company.get_absolute_url()

    def get_modal_url(self):
        return reverse('ajax_product_modal', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('catalogue:product_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('catalogue:product_delete', kwargs={'pk': self.id})

    def tag_image(self):
        return self.image.url if self.image else ''

    @staticmethod
    def filter_data(request, qs):
        q = request.GET.get('q', None)
        category_name = request.GET.getlist('category_name', None)
        if q:
            qs = qs.filter(title__icontains=q)
        qs = qs.filter(category__slug__in=category_name) if category_name else qs
        
        return qs


class ProductHitCounter(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='hits')
    session = models.CharField(max_length=220)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.save()

    def __str__(self):
        return self.product

    @staticmethod
    def update_hit(request, product):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        session = request.session.session_key
        qs = Product.objects.filter(product=product, session=session)
        if qs.exists():
            last_obj = qs.last()
            diff = datetime.datetime.today() - last_obj.timestamp.replace(tzinfo=None)
            if diff.days > 1:
                ProductHitCounter.objects.create(
                    product=product,
                    session=session
                )
        else:
            ProductHitCounter.objects.create(
                product=product,
                session=session
            )