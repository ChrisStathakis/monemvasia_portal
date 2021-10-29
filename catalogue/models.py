from django.db import models
from django.db.models import Sum, Q, F
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.text import slugify

import os, datetime
from decimal import Decimal
from tinymce.models import HTMLField
from .categories import Category
from companies.models import Company


class Product(models.Model):
    is_primary = models.BooleanField(default=False, )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='my_products')
    title = models.CharField(max_length=220)
    active = models.BooleanField(default=True)
    image = models.ImageField(blank=True, upload_to='products/', )
    is_offer = models.BooleanField(default=False, verbose_name='Προσφορά')
    category = models.ManyToManyField(Category, blank=True, verbose_name='Κατηγορία')
    notes = models.TextField(null=True, blank=True, verbose_name='Περιγραφή')
    objects = models.Manager()

    #  site
    sku = models.CharField(max_length=150, blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True, max_length=240, db_index=True)
    product_url = models.URLField(blank=True, null=True)

    # price sell and discount sells
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, verbose_name="Αρχική Τιμή")
    price_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Εκπτωτική Τιμή')
    final_price = models.DecimalField(default=0, decimal_places=2, max_digits=10, blank=True, verbose_name='Τιμή Πώλησης')
    
    def save(self, *args, **kwargs):
        if not self.product_url:
            self.product_url = self.company.detail.website
        self.final_price = self.price_discount if self.price_discount > 0 else self.price
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

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