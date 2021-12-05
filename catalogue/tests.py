from django.test import TestCase
from collections import OrderedDict
from .models import Product, Company
from datetime import datetime

class ProductTest(TestCase):

    def setUp(self):
        company1, _ = Company.objects.get_or_create(title='Company1', subscription_ends=datetime.now().date())
        company2, _ = Company.objects.get_or_create(title='La Grace',subscription_ends=datetime.now().date())
        blues, _ = Product.objects.get_or_create(title='Blue', company=company1)
        nike, _= Product.objects.get_or_create(title='Nike', company=company2, text='my blues sucks')
        bicycle, _ = Product.objects.get_or_create(title='Bicycle', company=company1)

    def test_product_search(self):
        product_queryset = Product.my_query.search('blue')
        print(product_queryset)


